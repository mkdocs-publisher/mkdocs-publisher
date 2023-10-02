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

import tempfile
from pathlib import Path

import pytest
import yaml
from _pytest.fixtures import SubRequest
from mkdocs.config.defaults import MkDocsConfig

from mkdocs_publisher.blog.plugin import BlogPlugin
from mkdocs_publisher.obsidian.plugin import ObsidianPlugin


@pytest.fixture()
def test_data_dir() -> Path:
    return Path().cwd() / "tests/_tests_data"


@pytest.fixture(scope="function")
def mkdocs_config(request: SubRequest) -> MkDocsConfig:
    """Fixture returning MkDocsConfig

    How to change configuration:

    ```python
    @pytest.mark.parametrize(
        "mkdocs_config",
        [{"docs_dir": "tests/_tests_data"}],
        indirect=True,
    )
    ```
    """
    try:
        config_dict = request.param
    except AttributeError:
        config_dict = {"docs_dir": "tests/_tests_data"}
    config = MkDocsConfig()
    with tempfile.NamedTemporaryFile(mode="w+") as config_file:
        yaml.safe_dump(data=config_dict, stream=config_file)
        config_file.seek(0)
        config.load_file(config_file=config_file)
        yield config  # type: ignore


@pytest.fixture(scope="function")
def pub_obsidian_plugin() -> ObsidianPlugin:
    plugin = ObsidianPlugin()
    plugin.load_config(options={"plugins": ["pub-obsidian"]})
    return plugin


@pytest.fixture(scope="function")
def pub_blog_plugin() -> BlogPlugin:
    plugin = BlogPlugin()
    plugin.load_config(options={"plugins": ["pub-blog"]})
    return plugin
