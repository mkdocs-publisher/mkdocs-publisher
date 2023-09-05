# MIT License
#
# Copyright (c) 2023 Maciej 'maQ' Kusz <maciej.kusz@gmail.com>
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
from typing import List
from typing import Optional
from uuid import uuid4

log = logging.getLogger(__name__)


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


def calculate_file_hash(file: Path, block_size: int = 8192) -> str:
    with open(file, "rb") as binary_file:
        file_hash = md5()
        while chunk := binary_file.read(block_size):
            file_hash.update(chunk)
        return file_hash.hexdigest()


def list_files(
    directory: Path, extensions: Optional[List[str]] = None, relative_to: Optional[Path] = None
) -> List[Path]:
    files_list: List[Path] = []
    for file in directory.iterdir():
        if file.is_dir():
            files_list.extend(
                list_files(directory=file, extensions=extensions, relative_to=relative_to)
            )
        elif str(file.suffix).lower() in extensions or extensions is None:  # type: ignore
            files_list.append(file if relative_to is None else file.relative_to(relative_to))
    return files_list


def get_hashed_file_name(file: Path) -> Path:
    return Path(file.with_name(f"{str(uuid4()).replace('-', '')}{str(file.suffix).lower()}").name)
