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
from collections import UserDict
from pathlib import Path
from typing import cast

from mkdocs.config.defaults import MkDocsConfig

from mkdocs_publisher._shared import mkdocs_utils
from mkdocs_publisher.blog.config import BlogPluginConfig
from mkdocs_publisher.meta.config import MetaPluginConfig
from mkdocs_publisher.obsidian.config import ObsidianPluginConfig

log = logging.getLogger("mkdocs.publisher._shared.publisher_utils")


def get_blog_dir(mkdocs_config: MkDocsConfig) -> Path | None:
    blog_config: BlogPluginConfig | Path | None = cast(
        BlogPluginConfig,
        mkdocs_utils.get_plugin_config(
            mkdocs_config=mkdocs_config,
            plugin_name="pub-blog",
        ),
    )

    blog_dir: Path | None = None
    if blog_config:
        blog_dir = Path(mkdocs_config.docs_dir).joinpath(blog_config.blog_dir)

    return blog_dir


def get_obsidian_dirs(mkdocs_config: MkDocsConfig) -> tuple[list[Path], Path | None]:
    ignored_dirs: list[Path] = []
    attachments_dir: Path | None = None
    docs_dir = Path(mkdocs_config.docs_dir)

    obsidian_config: ObsidianPluginConfig | None = cast(
        ObsidianPluginConfig,
        mkdocs_utils.get_plugin_config(
            mkdocs_config=mkdocs_config,
            plugin_name="pub-obsidian",
        ),
    )

    if obsidian_config:
        ignored_dirs.append(docs_dir.joinpath(obsidian_config.obsidian_dir))
        ignored_dirs.append(docs_dir.joinpath(obsidian_config.templates_dir))
        attachments_dir = docs_dir.joinpath(obsidian_config.attachments_dir)

    return ignored_dirs, attachments_dir


class PublisherFiles(UserDict):
    def __init__(self):
        self._on_serve: bool = False
        self._mkdocs_config: MkDocsConfig | None = None
        self._meta_plugin_config: MetaPluginConfig | None = None

        super().__init__()

    @property
    def on_serve(self) -> bool:
        return self._on_serve

    @on_serve.setter
    def on_serve(self, on_serve: bool):
        self._on_serve = on_serve

    def set_configs(self, mkdocs_config: MkDocsConfig, meta_plugin_config: MetaPluginConfig):
        self._mkdocs_config = mkdocs_config
        self._meta_plugin_config = meta_plugin_config

    def add_files(self):
        raise NotImplementedError
