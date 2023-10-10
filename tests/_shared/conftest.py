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

from pathlib import Path

import pytest

from mkdocs_publisher._shared import links


@pytest.fixture()
def relative_path_finder(test_data_dir: Path) -> links.RelativePathFinder:
    return links.RelativePathFinder(
        current_file_path=Path("current/file.md"),
        docs_dir=test_data_dir,
        relative_path=Path("relative"),
    )


@pytest.fixture()
def relative_sub_path_finder(test_data_dir: Path) -> links.RelativePathFinder:
    return links.RelativePathFinder(
        current_file_path=Path("current/cur_sub/cur_sub_file.md"),
        docs_dir=test_data_dir,
        relative_path=Path("relative"),
    )


@pytest.fixture()
def relative_blog_path_finder(test_data_dir: Path) -> links.RelativePathFinder:
    return links.RelativePathFinder(
        current_file_path=Path("relative/rel_file.md"),
        docs_dir=test_data_dir,
        relative_path=Path("relative"),
    )
