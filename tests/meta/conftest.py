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

import shutil
from pathlib import Path

import pytest
from _pytest.fixtures import SubRequest
from mkdocs.config.defaults import MkDocsConfig

from mkdocs_publisher._shared import mkdocs_utils
from mkdocs_publisher.meta.meta_files import MetaFile
from mkdocs_publisher.meta.meta_files import MetaFiles
from mkdocs_publisher.meta.meta_nav import MetaNav
from mkdocs_publisher.meta.plugin import MetaPluginConfig


@pytest.fixture(scope="function")
def mkdocs_config_with_docs_dir(
    request: SubRequest, tmp_path_factory: pytest.TempPathFactory
) -> tuple[MkDocsConfig, Path]:  # type: ignore [reportInvalidTypeForm]
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
        config_dict = {}
    if "docs_dir" not in config_dict:
        config_dict["docs_dir"] = "docs"
    docs_dir = tmp_path_factory.mktemp(config_dict["docs_dir"])
    config = MkDocsConfig()
    config.load_dict(patch=config_dict)

    yield (config, docs_dir)  # type: ignore [reportReportType]
    shutil.rmtree(path=docs_dir.parent, ignore_errors=True)


@pytest.fixture()
def patched_meta_files() -> MetaFiles:
    def patched_read_md_file(md_file_path: Path):
        _ = md_file_path
        return "", {}

    mkdocs_utils.read_md_file = patched_read_md_file
    meta_files: MetaFiles = MetaFiles()
    return meta_files


@pytest.fixture()
def patched_meta_nav(patched_meta_files: MetaFiles, mkdocs_config) -> MetaNav:
    def patched_get_metadata(meta_file: MetaFile, meta_file_path: Path):
        _, _ = meta_file, meta_file_path

    meta_plugin_config: MetaPluginConfig = MetaPluginConfig()  # type: ignore[reportAssignmentType]
    meta_plugin_config.validate()

    patched_meta_files.set_configs(
        mkdocs_config=mkdocs_config,
        meta_plugin_config=meta_plugin_config,
    )
    patched_meta_files._get_metadata = patched_get_metadata
    meta_nav: MetaNav = MetaNav(meta_files=patched_meta_files, blog_dir=Path("blog"))
    return meta_nav
