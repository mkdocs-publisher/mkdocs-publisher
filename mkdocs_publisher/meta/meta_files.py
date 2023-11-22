# MIT License
#
# Copyright (c) 2024 Maciej 'maQ' Kusz <maciej.kusz@gmail.com>
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
import re
from collections import UserDict
from dataclasses import dataclass
from dataclasses import field
from pathlib import Path
from typing import Any
from typing import Optional

from mkdocs.config.defaults import MkDocsConfig
from mkdocs.structure.files import File
from mkdocs.utils import meta as meta_parser

# noinspection PyProtectedMember
from mkdocs_publisher._shared.urls import create_slug
from mkdocs_publisher.meta.config import MetaPluginConfig
from mkdocs_publisher.meta.config import OverviewChoiceEnum
from mkdocs_publisher.meta.config import PublishChoiceEnum
from mkdocs_publisher.meta.config import TitleChoiceEnum

log = logging.getLogger("mkdocs.plugins.publisher._shared.meta_files")


HEADINGS_RE = re.compile(r"^#+ (?P<title>[^|#\r\n\t\f\v]+)$")


@dataclass
class MetaFile:
    path: Path
    abs_path: Path
    is_dir: bool
    is_overview: bool = field(default=False)
    is_hidden: bool = field(default=False)
    is_draft: Optional[bool] = field(default=None)
    title: Optional[str] = field(default=None)
    slug: Optional[str] = field(default=None)
    file: Optional[File] = field(default=None)

    @property
    def name(self) -> str:
        return self.path.name

    @property
    def parent(self) -> Optional[Path]:
        parent = self.path.parent
        if str(parent) == ".":
            parent = None
        return parent


class MetaFiles(UserDict):
    def __init__(self):
        self._on_serve: bool = False
        self._mkdocs_config: Optional[MkDocsConfig] = None
        self._meta_plugin_config: Optional[MetaPluginConfig] = None
        self._hidden_paths: list[Path] = []
        super().__init__()

    @property
    def meta_file(self) -> str:
        return self._meta_plugin_config.dir_meta_file

    @property
    def on_serve(self) -> bool:
        return self._on_serve

    @on_serve.setter
    def on_serve(self, on_serve: bool):
        self._on_serve = on_serve

    def add_hidden_path(self, hidden_path: Optional[Path]):
        if hidden_path is not None:
            self._hidden_paths.append(hidden_path.relative_to(self._mkdocs_config.docs_dir))

    def set_configs(self, mkdocs_config: MkDocsConfig, meta_plugin_config: MetaPluginConfig):
        self._mkdocs_config = mkdocs_config
        self._meta_plugin_config = meta_plugin_config

    @staticmethod
    def _read_md_file(meta_file_path: Path) -> tuple[str, dict[str, Any]]:  # pragma: no cover
        with meta_file_path.open(encoding="utf-8-sig", errors="strict") as md_file:
            # Add empty line at the end of file and read all data
            return meta_parser.get_data(f"{md_file.read()}\n")

    def _get_title(self, meta_file: MetaFile, meta: dict[str, Any], markdown: str):
        title: Optional[str] = None
        mode = self._meta_plugin_config.title.mode

        if mode == TitleChoiceEnum.META:
            title = meta.get(self._meta_plugin_config.title.key_name)
            if title is None and self._meta_plugin_config.title.warn_on_missing_meta:
                log.warning(
                    f'Title value from "{self._meta_plugin_config.title.key_name}" meta data '
                    f'is missing for file: "{str(meta_file.path)}"'
                )

        if title is None and (mode == TitleChoiceEnum.META or mode == TitleChoiceEnum.HEAD):
            headings = re.findall(HEADINGS_RE, markdown)
            title = str(headings[0]).strip() if len(headings) > 0 else None
            if title is None and self._meta_plugin_config.title.warn_on_missing_header:
                log.warning(
                    f'Title value from first heading is missing for file: "{str(meta_file.path)}"'
                )

        if title is None and (mode == TitleChoiceEnum.META or mode == TitleChoiceEnum.FILE):
            title = str(meta_file.path.stem).replace("_", " ").title()

        meta_file.title = title

    def _get_slug(self, meta_file: MetaFile, meta: dict[str, Any]):
        meta_file.slug = create_slug(  # pragma: no cover (covered separately)
            file_name=meta_file.path.stem,
            slug_mode=self._meta_plugin_config.slug.mode,
            slug=meta.get(self._meta_plugin_config.slug.key_name),
            title=meta_file.title,
            warn_on_missing=self._meta_plugin_config.slug.warn_on_missing,
        )

    def _get_overview(self, meta_file: MetaFile, meta: dict[str, Any], markdown: str):
        """Overview works only for metafiles ("README.md", "index.md") that are detected as dir"""
        if not meta_file.is_dir:
            meta_file.is_overview = False
        else:
            is_overview = meta.get(
                self._meta_plugin_config.overview.key_name,
                self._meta_plugin_config.overview.default,
            )
            if is_overview == OverviewChoiceEnum.AUTO:
                meta_file.is_overview = bool(len(markdown.strip()))
            else:
                meta_file.is_overview = is_overview

    def _get_publish_status(self, meta_file: MetaFile, meta: dict[str, Any]):
        publish = meta.get(str(self._meta_plugin_config.publish.key_name), None)

        # Get default values if publish status is not specified
        if publish is None:
            if meta_file.is_dir:
                publish = self._meta_plugin_config.publish.dir_default
                if self._meta_plugin_config.publish.dir_warn_on_missing:
                    log.warning(
                        f'Missing "{self._meta_plugin_config.publish.key_name}" value in '
                        f'file "{meta_file.path}". Setting to '
                        f'default value: "{self._meta_plugin_config.publish.dir_default}".'
                    )
            else:
                publish = self._meta_plugin_config.publish.file_default
                if self._meta_plugin_config.publish.file_warn_on_missing:
                    log.warning(
                        f'Missing "{self._meta_plugin_config.publish.key_name}" value in '
                        f'file "{meta_file.path}". Setting to '
                        f'default value: "{self._meta_plugin_config.publish.file_default}".'
                    )

        # Override some values inherited from parent
        if meta_file.parent is not None:
            meta_file_parent: MetaFile = self[str(meta_file.parent)]

            if meta_file_parent.is_draft:
                publish = False
            if meta_file_parent.is_hidden:
                publish = PublishChoiceEnum.HIDDEN

        # When live preview is running, all pages are visible
        if self._on_serve:
            publish = True

        # Set values depends on publish status
        if meta_file.path in self._hidden_paths or publish == PublishChoiceEnum.HIDDEN:
            meta_file.is_hidden = True
            meta_file.is_draft = False
        elif publish in PublishChoiceEnum.drafts():
            meta_file.is_hidden = False
            meta_file.is_draft = True
        elif publish in PublishChoiceEnum.published():
            meta_file.is_hidden = False
            meta_file.is_draft = False
        else:
            log.warning(
                f'Wrong key "{self._meta_plugin_config.publish.key_name}" value '
                f'({publish}) in file "{meta_file.path}" (only '
                f"{PublishChoiceEnum.choices()} are possible)"
            )

    # Coverage skipped because each method is covered separately.
    def _get_metadata(self, meta_file: MetaFile, meta_file_path: Path):  # pragma: no cover
        # Order of method execution is crucial for reading all values.
        markdown, meta = self._read_md_file(meta_file_path=meta_file_path)

        self._get_title(meta_file=meta_file, meta=meta, markdown=markdown)
        self._get_slug(meta_file=meta_file, meta=meta)
        if self._meta_plugin_config.overview.enabled:
            self._get_overview(meta_file=meta_file, meta=meta, markdown=markdown)
        self._get_publish_status(meta_file=meta_file, meta=meta)

        log.debug(meta_file)

    def __setitem__(self, path: str, meta_file: MetaFile):
        if meta_file.is_dir:
            meta_file_exists = False

            # Calculate properties based on meta file metadata
            meta_file_path = meta_file.abs_path.joinpath(self._meta_plugin_config.dir_meta_file)
            if meta_file_path.exists():
                meta_file_exists = True
                self._get_metadata(meta_file=meta_file, meta_file_path=meta_file_path)

            if not meta_file_exists:
                meta_file.title = str(meta_file.path.stem)
                meta_file.slug = create_slug(
                    file_name=str(meta_file.name),
                    slug_mode=self._meta_plugin_config.slug.mode,
                    slug=meta_file.path.stem,
                    title=meta_file.title,
                    warn_on_missing=self._meta_plugin_config.slug.warn_on_missing,
                )
                meta_file.is_draft = not self._meta_plugin_config.publish.dir_default
        else:
            self._get_metadata(meta_file=meta_file, meta_file_path=meta_file.abs_path)

        super().__setitem__(path, meta_file)

    def drafts(self, files: bool = False, dirs: bool = False) -> dict[str, MetaFile]:
        draft_files = {}
        for path, meta_file in self.items():
            if meta_file.is_draft and (
                (files and not dirs and not meta_file.is_dir)
                or (not files and dirs and meta_file.is_dir)
                or (not files and not dirs)
            ):
                draft_files[path] = meta_file
        return draft_files

    def hidden(self, files: bool = False, dirs: bool = False) -> dict[str, MetaFile]:
        hidden_files = {}
        for path, meta_file in self.items():
            if meta_file.is_hidden and (
                (files and not dirs and not meta_file.is_dir)
                or (not files and dirs and meta_file.is_dir)
                or (not files and not dirs)
            ):
                hidden_files[path] = meta_file
        return hidden_files
