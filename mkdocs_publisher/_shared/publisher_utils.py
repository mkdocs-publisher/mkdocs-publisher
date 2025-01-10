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
from pathlib import Path
from typing import Optional
from typing import Union
from typing import cast

from mkdocs.config.defaults import MkDocsConfig

from mkdocs_publisher._shared import mkdocs_utils
from mkdocs_publisher.blog.config import BlogPluginConfig
from mkdocs_publisher.obsidian.config import ObsidianPluginConfig

log = logging.getLogger("mkdocs.publisher._shared.publisher_utils")


def get_blog_dir(mkdocs_config: MkDocsConfig) -> Optional[Path]:
    blog_config: Optional[Union[BlogPluginConfig, Path]] = cast(
        BlogPluginConfig,
        mkdocs_utils.get_plugin_config(
            mkdocs_config=mkdocs_config,
            plugin_name="pub-blog",
        ),
    )
    if blog_config is not None:
        blog_config = Path(mkdocs_config.docs_dir).joinpath(blog_config.blog_dir)

    return blog_config


def get_obsidian_dirs(mkdocs_config: MkDocsConfig) -> tuple[list[Path], Optional[Path]]:
    ignored_dirs: list[Path] = []
    attachments_dir: Optional[Path] = None
    docs_dir = Path(mkdocs_config.docs_dir)

    obsidian_config: Optional[ObsidianPluginConfig] = cast(
        ObsidianPluginConfig,
        mkdocs_utils.get_plugin_config(
            mkdocs_config=mkdocs_config,
            plugin_name="pub-obsidian",
        ),
    )
    if obsidian_config is not None:
        ignored_dirs.append(docs_dir.joinpath(obsidian_config.obsidian_dir))
        ignored_dirs.append(docs_dir.joinpath(obsidian_config.templates_dir))
        attachments_dir = docs_dir.joinpath(obsidian_config.attachments_dir)

    return ignored_dirs, attachments_dir
