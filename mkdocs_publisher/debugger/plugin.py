# MIT License
#
# Copyright (c) 2023-2025 Maciej 'maQ' Kusz <maciej.kusz@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import logging
import platform
import sys
from io import BytesIO
from pathlib import Path
from zipfile import ZIP_DEFLATED
from zipfile import ZipFile

from mkdocs.config.defaults import MkDocsConfig
from mkdocs.plugins import BasePlugin
from mkdocs.plugins import event_priority

from mkdocs_publisher._shared import file_utils
from mkdocs_publisher._shared import mkdocs_utils
from mkdocs_publisher.debugger import loggers
from mkdocs_publisher.debugger.config import DebuggerPluginConfig

log = logging.getLogger("mkdocs.publisher.debug.plugin")

LOG_FILENAME_SUFFIX = "_mkdocs_build.log"  # TODO: make it configurable
ZIP_FILENAME_SUFFIX = "_mkdocs_debug.zip"  # TODO: make it configurable
FILES_TO_ZIP_LIST = [
    "mkdocs.yml",
    "requirements.txt",
    "pyproject.toml",
    "poetry.lock",
    ".gitignore",
]
PIP_FREEZE_FILENAME = "requirements_pub_debugger.txt"  # TODO: make it configurable


class DebuggerPlugin(BasePlugin[DebuggerPluginConfig]):
    supports_multiple_instances = False

    def __init__(self):
        self._mkdocs_log_stream_handler: logging.Handler = logging.getLogger("mkdocs").handlers[0]

        self._mkdocs_log_file_handler: loggers.DatedFileHandler = loggers.DatedFileHandler(
            filename=f"%Y%m%d_%H%M%S{LOG_FILENAME_SUFFIX}",
        )

        self._mkdocs_log_file: str = str(Path(self._mkdocs_log_file_handler.baseFilename).name)
        self._mkdocs_log_date: str = self._mkdocs_log_file.replace(LOG_FILENAME_SUFFIX, "")
        self._mkdocs_config: MkDocsConfig = mkdocs_utils.get_mkdocs_config()

        self.config: DebuggerPluginConfig = mkdocs_utils.get_plugin_config(
            plugin_config_type=DebuggerPluginConfig,  # type: ignore[reportArgumentType]
            mkdocs_config=self._mkdocs_config,
        )  # type: ignore[reportAttributeAccessIssue]

        if self.config.console_log.enabled:
            self._mkdocs_log_stream_handler.setFormatter(
                loggers.ProjectPathStreamFormatter(console_config=self.config.console_log),
            )
            self._mkdocs_log_stream_handler.addFilter(
                loggers.ProjectPathConsoleFilter(console_config=self.config.console_log),
            )
            # noinspection PyUnresolvedReferences
            mkdocs_log_level = logging.getLogger("mkdocs").level
            console_log_level = logging._nameToLevel[self.config.console_log.log_level]  # noqa: SLF001

            if mkdocs_log_level <= console_log_level:
                console_log_level = mkdocs_log_level

            self._mkdocs_log_stream_handler.setLevel(console_log_level)
            logging.getLogger("root").handlers = [self._mkdocs_log_stream_handler]
            logging.getLogger("mkdocs").setLevel(console_log_level)

        if self.config.file_log.enabled:
            self._mkdocs_log_file_handler.setFormatter(
                loggers.ProjectPathFileFormatter(
                    fmt=self.config.file_log.log_format,
                    datefmt=self.config.file_log.time_format,
                ),
            )
            self._mkdocs_log_file_handler.addFilter(loggers.ProjectPathFileFilter(file_config=self.config.file_log))
            # noinspection PyUnresolvedReferences
            self._mkdocs_log_file_handler.setLevel(logging._nameToLevel[self.config.file_log.log_level])  # noqa: SLF001

            logging.getLogger("mkdocs").handlers.append(self._mkdocs_log_file_handler)

            if self.config.file_log.remove_old_files:
                for log_file in Path().rglob(f"*{LOG_FILENAME_SUFFIX}"):
                    if str(log_file) != self._mkdocs_log_file:
                        log_file.unlink(missing_ok=True)

    @event_priority(100)  # Run after all other plugins
    def on_shutdown(self) -> None:
        if self.config.file_log.enabled:
            log.info(f"Platform: {platform.platform()}")
            log.info(
                f"Python version: {platform.python_version()} "
                f"(using virtual environment: {str(sys.prefix != sys.base_prefix).lower()})",
            )
            log.info(f"Build log file: {self._mkdocs_log_file_handler.baseFilename}")

        if self.config.zip_log.enabled:
            zip_file_name = f"{self._mkdocs_log_date}{ZIP_FILENAME_SUFFIX}"

            if self.config.zip_log.remove_old_files:
                for log_file in Path().rglob(f"*{ZIP_FILENAME_SUFFIX}"):
                    if str(log_file) != zip_file_name:
                        log_file.unlink(missing_ok=True)

            archive = BytesIO()
            with ZipFile(archive, "a", ZIP_DEFLATED, False) as archive_file:
                # Zip files from list
                for file_to_zip in FILES_TO_ZIP_LIST:
                    if Path(file_to_zip).exists():
                        log.debug(f"File: {file_to_zip} added to archive")
                        archive_file.write(filename=file_to_zip, arcname=file_to_zip)
                    else:
                        log.debug(f"File: {file_to_zip} doesn't exists and not added to archive")

                # Write pip freeze as file
                if self.config.zip_log.add_pip_freeze:
                    pip_run = file_utils.run_subprocess(["pip", "freeze", "--local"])
                    archive_file.writestr(
                        zinfo_or_arcname=PIP_FREEZE_FILENAME,
                        data=pip_run.stdout.decode("utf-8"),
                    )

                # Write build log file
                archive_file.write(filename=self._mkdocs_log_file, arcname=self._mkdocs_log_file)

            with Path(zip_file_name).open("wb") as zip_file:
                zip_file.write(archive.getvalue())
                log.info(f"Debugger ZIP file: {zip_file_name}")
