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

from pathlib import Path

import pytest
from _pytest.fixtures import SubRequest
from mkdocs.config.defaults import MkDocsConfig

from mkdocs_publisher.meta.meta_files import MetaFiles
from mkdocs_publisher.meta.meta_nav import MetaNav


@pytest.fixture(scope="function")
def mkdocs_config(request: SubRequest) -> MkDocsConfig:  # type: ignore
    """Fixture returning MkDocsConfig

    How to change configuration:

    ```python
    @pytest.mark.parametrize(
        "mkdocs_config",
        [{"docs_dir": "tests/_tests_data"}],
        indirect=True,
    )
    def test_function(mkdocs_config):
    ```
    """
    try:
        config_dict = request.param
    except AttributeError:
        config_dict = {"docs_dir": "/Users/me"}
    config = MkDocsConfig()
    config.load_dict(patch=config_dict)
    yield config  # type: ignore


@pytest.fixture()
def patched_meta_files() -> MetaFiles:
    def patch_read_md_file(meta_file_path: Path):
        _ = meta_file_path
        return "", {}

    meta_files: MetaFiles = MetaFiles()
    meta_files._read_md_file = patch_read_md_file  # monkey patch
    return meta_files


@pytest.fixture()
def meta_nav(patched_meta_files: MetaFiles) -> MetaNav:
    meta_nav: MetaNav = MetaNav(meta_files=patched_meta_files)
    return meta_nav
