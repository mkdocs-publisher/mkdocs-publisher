# MIT License
#
# Copyright (c) 2023-2024 Maciej 'maQ' Kusz <maciej.kusz@gmail.com>
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
from typing import Optional
from uuid import uuid4

log = logging.getLogger("mkdocs.publisher._shared.file_utils")


def run_subprocess(cmd, capture_output: bool = True) -> subprocess.CompletedProcess:
    cmd = [arg for arg in cmd if arg is not None]
    log.debug(f"Run cmd: {' '.join(cmd)}")
    return subprocess.run(cmd, capture_output=capture_output)


def remove_dir(directory: Path):
    for file in directory.iterdir():
        if file.is_dir():
            remove_dir(directory=file)
            file.rmdir()
        else:
            file.unlink(missing_ok=True)


def calculate_file_hash(file: Path, block_size: int = 65536) -> Optional[str]:
    try:
        with open(file, "rb") as binary_file:
            file_hash = md5()
            while chunk := binary_file.read(block_size):
                file_hash.update(chunk)
            return file_hash.hexdigest()
    except IsADirectoryError:
        return None


def list_files(
    directory: Path,
    extensions: Optional[list[str]] = None,
    exclude: Optional[list[str]] = None,
) -> list[Path]:
    temp_files_list: list[Path] = []
    extensions = [] if extensions is None else extensions
    exclude = [] if exclude is None else exclude
    for ext in extensions:
        for file in directory.glob(f"**/*{ext}"):
            temp_files_list.append(file.relative_to(directory))

    excluded_files_list: list[Path] = []
    for exc in exclude:
        for file in directory.rglob(exc):
            excluded_files_list.append(file.relative_to(directory))

    files_list: list[Path] = [file for file in temp_files_list if file not in excluded_files_list]
    return files_list


def get_hashed_file_name(file: Path) -> Path:
    return Path(file.with_name(f"{str(uuid4()).replace('-', '')}{str(file.suffix).lower()}").name)
