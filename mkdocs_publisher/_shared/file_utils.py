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
import subprocess
from hashlib import md5
from pathlib import Path
from uuid import uuid4

from mkdocs.config.defaults import MkDocsConfig
from mkdocs.structure.files import Files

log = logging.getLogger("mkdocs.publisher._shared.file_utils")


def run_subprocess(cmd, capture_output: bool = True) -> subprocess.CompletedProcess:  # noqa: ANN001
    cmd = [arg for arg in cmd if arg is not None]
    log.debug(f"Run cmd: {' '.join(cmd)}")
    return subprocess.run(cmd, capture_output=capture_output, check=False)  # noqa: S603


def remove_dir(directory: Path) -> None:
    # for file in directory.iterdir():
    #     if file.is_dir():
    #         remove_dir(directory=file)
    #         file.rmdir()
    #     else:
    #         file.unlink(missing_ok=True)
    pass


def calculate_file_hash(file: Path, block_size: int = 65536) -> str | None:
    try:
        with Path(file).open(mode="rb") as binary_file:
            file_hash = md5()  # noqa: S324
            while chunk := binary_file.read(block_size):
                file_hash.update(chunk)
            return file_hash.hexdigest()
    except (IsADirectoryError, FileNotFoundError):
        return None


class FilesList:
    def __init__(
        self,
        mkdocs_config: MkDocsConfig,
        files: Files,
        exclude: list[Path] | None = None,
    ) -> None:
        self._mkdocs_config: MkDocsConfig = mkdocs_config
        self._all_files: Files = files
        self._exclude: list[Path] = [] if exclude is None else exclude

    def list_files(self, extension: list[str], exclude: list[Path]) -> None:
        excluded = [*exclude, *self._exclude]
        for file in self._all_files:
            if Path(file.dest_path).suffix.lower() in extension and not any(
                Path(file.dest_path).is_relative_to(e) for e in excluded
            ):
                # log.critical(file.dest_path)
                pass


def list_files(
    directory: Path,
    extensions: list[str] | None = None,
    exclude: list[str] | None = None,
) -> list[Path]:
    files_list: list[Path] = []
    extensions = [] if extensions is None else extensions
    exclude = [] if exclude is None else exclude

    excluded_files_list: list[Path] = [file.relative_to(directory) for exc in exclude for file in directory.rglob(exc)]

    for ext in extensions:
        for file in directory.glob(f"**/*{ext}"):
            file_relative_path = file.relative_to(directory)
            for exc in excluded_files_list:
                log.warning(exc)
                log.warning(str(file_relative_path).startswith(str(exc)))

            files_list.extend(
                file.relative_to(directory)
                for exc in excluded_files_list
                if not str(file_relative_path).startswith(str(exc))
            )

    return files_list


def get_hashed_file_name(file: Path) -> Path:
    return Path(file.with_name(f"{str(uuid4()).replace('-', '')}{str(file.suffix).lower()}").name)
