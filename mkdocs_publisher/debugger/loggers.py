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

import datetime
import logging
import re
import site
from pathlib import Path

import colorama

from mkdocs_publisher.debugger.config import _DebuggerConsoleConfig
from mkdocs_publisher.debugger.config import _DebuggerFileConfig

colorama.init()

LIVERELOAD_MSG_RE = re.compile(r"(?P<time>\[\d{,2}:\d{1,2}:\d{,2}] )?(?P<text>.*)")
DEPRECATION_MSG_RE = re.compile(r"^(?P<deprecation>DeprecationWarning:)")
SITE_PACKAGES_DIR = Path(site.getsitepackages()[0])
LOG_LEVEL_COLOR_MAPPING = {
    logging.DEBUG: colorama.Fore.BLUE,
    logging.INFO: colorama.Fore.GREEN,
    logging.WARNING: colorama.Fore.YELLOW,
    logging.ERROR: colorama.Fore.RED,
    logging.CRITICAL: colorama.Fore.RED,
}


class DatedFileHandler(logging.FileHandler):
    def __init__(self, filename):
        dated_filename = datetime.datetime.now(tz=datetime.timezone.utc).strftime(str(filename))
        Path(dated_filename).parent.mkdir(parents=True, exist_ok=True)
        super().__init__(filename=dated_filename)


class ProjectPathStreamFormatter(logging.Formatter):
    def __init__(self, console_config: _DebuggerConsoleConfig):
        self._console_config: _DebuggerConsoleConfig = console_config

        super().__init__()

    @staticmethod
    def _livereload_msg_strip_time(match: re.Match) -> str:
        return match.groupdict()["text"]

    def format(self, record: logging.LogRecord) -> str:
        path = Path(record.pathname)
        try:
            record.project_path = str(path.relative_to(path.cwd()))
        except ValueError:
            record.project_path = str(path)

        fmt = "%(project_path)s:%(lineno)d " if self._console_config.show_code_link else ""

        if self._console_config.show_entry_time:
            fmt = f"{fmt}{colorama.Fore.MAGENTA}%(asctime)s{colorama.Fore.RESET} "

        fmt = (
            f'{fmt}[{LOG_LEVEL_COLOR_MAPPING.get(record.levelno) or ""}'
            f"%(levelname)-5.5s{colorama.Fore.RESET}] %(message)s"
        )

        if self._console_config.show_logger_name:
            fmt = f"{fmt} {colorama.Fore.CYAN}[%(name)s]{colorama.Fore.RESET}"

        self._style._fmt = fmt  # noqa: SLF001
        self.datefmt = str(self._console_config.time_format).replace("%f", str(record.msecs)[0:3])

        if self._console_config.show_entry_time:
            record.msg = re.sub(LIVERELOAD_MSG_RE, self._livereload_msg_strip_time, str(record.msg))

        return super().format(record=record)


class ProjectPathFileFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        project_file_path = Path(record.pathname)
        try:
            record.project_path = str(
                project_file_path.relative_to(
                    SITE_PACKAGES_DIR if "site-packages" in str(project_file_path) else project_file_path.cwd(),
                ),
            )
        except ValueError:
            record.project_path = str(project_file_path)

        return super().format(record=record)


class ProjectPathConsoleFilter(logging.Filter):
    def __init__(self, console_config: _DebuggerConsoleConfig):
        self._console_config: _DebuggerConsoleConfig = console_config
        super().__init__()

    def filter(self, record):
        if (
            not self._console_config.show_deprecation_warnings
            and isinstance(record.msg, str)
            and re.findall(DEPRECATION_MSG_RE, record.msg)
        ):
            return None
        return record if record.name not in self._console_config.filter_logger_names else None


class ProjectPathFileFilter(logging.Filter):
    def __init__(self, file_config: _DebuggerFileConfig):
        self._file_config: _DebuggerFileConfig = file_config
        super().__init__()

    def filter(self, record):
        return record if record.name not in self._file_config.filter_logger_names else None
