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
from collections import UserDict
from dataclasses import dataclass
from dataclasses import field
from pathlib import Path
from typing import NoReturn
from typing import Sequence  # noqa: UP035

from mkdocs.config.defaults import MkDocsConfig
from mkdocs.structure.nav import Link
from mkdocs.structure.nav import Section
from mkdocs.structure.pages import Page

from mkdocs_publisher._shared import mkdocs_utils
from mkdocs_publisher.meta.config import MetaPluginConfig
from mkdocs_publisher.obsidian.config import ObsidianPluginConfig

log = logging.getLogger("mkdocs.publisher._shared.publisher_utils")


def get_obsidian_dirs(mkdocs_config: MkDocsConfig) -> tuple[list[Path], Path | None]:
    ignored_dirs: list[Path] = []
    attachments_dir: Path | None = None
    docs_dir = Path(mkdocs_config.docs_dir)

    obsidian_config: ObsidianPluginConfig | None = mkdocs_utils.get_plugin_config(
        plugin_config_type=ObsidianPluginConfig,  # type: ignore[reportArgumentType]
        mkdocs_config=mkdocs_config,
    )  # type: ignore[reportAssignmentType]

    if obsidian_config:
        ignored_dirs.append(docs_dir.joinpath(obsidian_config.obsidian_dir))
        ignored_dirs.append(docs_dir.joinpath(obsidian_config.templates_dir))
        attachments_dir = docs_dir.joinpath(obsidian_config.attachments_dir)

    return ignored_dirs, attachments_dir


@dataclass
class PublisherFile:
    path: Path
    abs_path: Path = field(repr=False)
    is_dir: bool = field(default=False)
    is_draft: bool | None = field(default=None)
    slug: str | None = field(default=None)
    title: str | None = field(default=None)


@dataclass
class PublisherTitleConfig:
    key_name: str


@dataclass
class PublisherFilesConfig:
    title: PublisherTitleConfig


class PublisherFiles(UserDict):
    def __init__(self) -> None:
        self._on_serve: bool = False
        self._mkdocs_config: MkDocsConfig | None = None
        self._meta_plugin_config: MetaPluginConfig | None = None
        self._config: PublisherFilesConfig | None = None

        super().__init__()

    @property
    def on_serve(self) -> bool:
        return self._on_serve

    @on_serve.setter
    def on_serve(self, on_serve: bool) -> None:
        self._on_serve = on_serve

    def set_configs(self, mkdocs_config: MkDocsConfig, meta_plugin_config: MetaPluginConfig) -> None:
        self._mkdocs_config = mkdocs_config
        self._meta_plugin_config = meta_plugin_config

    def add_files(self) -> NoReturn:
        raise NotImplementedError  # pragma: no cover


def nav_cleanup(items, removal_list: Sequence[str | Path]) -> list:  # noqa: ANN001
    removal_list = [str(p) for p in removal_list]
    nav = []
    for item in items:
        if isinstance(item, Section):
            item.children = nav_cleanup(items=item.children, removal_list=removal_list)
            # If section is empty, skip it
            if len(item.children) > 0:
                nav.append(item)
        elif (
            isinstance(item, Page)
            and str(item.file.src_path) not in removal_list
            and str(Path(item.file.src_path).parent) not in removal_list
        ) or (isinstance(item, Link) and item.title not in removal_list):
            nav.append(item)
    return nav
