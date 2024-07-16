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
import re
from collections import UserDict
from collections.abc import Generator
from dataclasses import dataclass
from dataclasses import field
from functools import cached_property
from pathlib import Path
from typing import Any
from typing import Optional
from urllib.parse import quote

from mkdocs.config.defaults import MkDocsConfig
from mkdocs.structure.files import File
from mkdocs.structure.files import Files
from mkdocs.utils import meta as meta_parser

from mkdocs_publisher._shared import links
from mkdocs_publisher._shared import templates
from mkdocs_publisher._shared.urls import create_slug
from mkdocs_publisher.meta.config import MetaPluginConfig
from mkdocs_publisher.meta.config import OverviewChoiceEnum
from mkdocs_publisher.meta.config import PublishChoiceEnum
from mkdocs_publisher.meta.config import TitleChoiceEnum

log = logging.getLogger("mkdocs.publisher._shared.meta_files")


HEADINGS_RE = re.compile(r"^#+ (?P<title>[^|#\r\n\t\f\v]+)$")


@dataclass
class MetaFile:
    is_dir: bool
    path: Path
    abs_path: Path = field(repr=False)
    file: Optional[File] = field(default=None, repr=False)
    is_draft: Optional[bool] = field(default=None)
    is_hidden: bool = field(default=False)
    is_overview: bool = field(default=False)
    redirect: Optional[str] = field(default=None)
    slug: Optional[str] = field(default=None)
    title: Optional[str] = field(default=None)
    url: Optional[str] = field(default=None)

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
        """Calculate title for given file"""

        title: Optional[str] = None
        mode = self._meta_plugin_config.title.mode
        if mode == TitleChoiceEnum.META:
            title = meta.get(self._meta_plugin_config.title.key_name)
            if (
                title is None
                and self._meta_plugin_config.title.warn_on_missing_meta
                and not (meta_file.is_draft or (meta_file.is_dir and not meta_file.is_overview))
            ):
                log.warning(
                    f'Title value from "{self._meta_plugin_config.title.key_name}" meta data '
                    f'is missing for file: "{str(meta_file.path)}"'
                )

        if title is None and (mode == TitleChoiceEnum.META or mode == TitleChoiceEnum.HEAD):
            headings = re.findall(HEADINGS_RE, markdown)
            title = str(headings[0]).strip() if len(headings) > 0 else None
            if (
                title is None
                and self._meta_plugin_config.title.warn_on_missing_header
                and not (meta_file.is_draft or (meta_file.is_dir and not meta_file.is_overview))
            ):
                log.warning(f'Title value from first heading is missing for file: "{str(meta_file.path)}"')

        if title is None and (mode == TitleChoiceEnum.META or mode == TitleChoiceEnum.FILE):
            title = str(meta_file.path.stem).replace("_", " ").title()

        meta_file.title = title

    def _get_slug(self, meta_file: MetaFile, meta: dict[str, Any]):
        """Calculate slug for given file"""

        meta_file.slug = create_slug(  # pragma: no cover
            file_name=meta_file.path.stem,
            slug_mode=self._meta_plugin_config.slug.mode,
            slug=meta.get(self._meta_plugin_config.slug.key_name),
            title=meta_file.title,
            warn_on_missing=self._meta_plugin_config.slug.warn_on_missing,
        )

    def _get_redirect(self, meta_file: MetaFile, meta: dict[str, Any], markdown: str) -> dict[str, Any]:
        """Determine if given file is a redirection"""

        redirect = meta.get(self._meta_plugin_config.redirect.key_name, None)
        relative_path_finder = links.RelativePathFinder(
            current_file_path=meta_file.path,
            docs_dir=Path(self._mkdocs_config.docs_dir),
            relative_path=meta_file.path,
        )

        if redirect is False:
            redirect = None
        elif redirect is True:
            if match := re.search(links.RELATIVE_LINK_RE, markdown):
                link = links.RelativeLinkMatch(**match.groupdict(), relative_path_finder=relative_path_finder)
                anchor = f"#{link.anchor}" if link.anchor else ""
                redirect = f"{link.link}{anchor}"

            elif match := re.search(links.URL_RE_PART, markdown):
                redirect = match.groupdict()["link"]
            else:
                redirect = None

        meta[self._meta_plugin_config.redirect.key_name] = redirect

        if isinstance(redirect, str) and not re.search(links.URL_RE_PART, redirect):
            # Document with redirection should be hidden
            meta[self._meta_plugin_config.publish.key_name] = PublishChoiceEnum.HIDDEN.name.lower()

        meta_file.redirect = redirect  # type: ignore

        return meta

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
        """Calculate publication status for given file"""

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
            if meta_file_parent.is_hidden and publish not in PublishChoiceEnum.drafts():
                publish = PublishChoiceEnum.HIDDEN.name.lower()

        # When live preview is running, all pages are visible
        if self._on_serve and not meta_file.is_hidden:
            publish = True

        if publish not in PublishChoiceEnum.choices():
            publish = self._meta_plugin_config.publish.file_default
            log.warning(
                f'Wrong key "{self._meta_plugin_config.publish.key_name}" value '
                f'({publish}) in file "{meta_file.path}" (only '
                f"{PublishChoiceEnum.choices()} are possible)"
            )

        # Set values depends on publish status
        if meta_file.path in self._hidden_paths or publish == PublishChoiceEnum.HIDDEN:
            meta_file.is_hidden = True
            meta_file.is_draft = False
        elif publish in PublishChoiceEnum.published():
            meta_file.is_hidden = False
            meta_file.is_draft = False
        else:
            meta_file.is_hidden = False
            meta_file.is_draft = True

    def _get_metadata(self, meta_file: MetaFile, meta_file_path: Path):  # pragma: no cover
        """Read all metadata values for given file"""

        markdown, meta = self._read_md_file(meta_file_path=meta_file_path)

        # Order of method execution is crucial for reading all values.
        meta = self._get_redirect(meta_file=meta_file, meta=meta, markdown=markdown)
        if self._meta_plugin_config.overview.enabled:
            self._get_overview(meta_file=meta_file, meta=meta, markdown=markdown)
        self._get_publish_status(meta_file=meta_file, meta=meta)
        self._get_title(meta_file=meta_file, meta=meta, markdown=markdown)
        self._get_slug(meta_file=meta_file, meta=meta)

    def __setitem__(self, path: str, meta_file: MetaFile):
        """Add file"""

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

    def _drafts(self, files: bool = False, dirs: bool = False) -> dict[str, MetaFile]:
        """Returns draft files and/or directories"""

        draft_files = {}
        for path, meta_file in self.items():
            if meta_file.is_draft and (
                (files and not dirs and not meta_file.is_dir)
                or (not files and dirs and meta_file.is_dir)
                or (not files and not dirs)
            ):
                draft_files[path] = meta_file
            elif files and meta_file.is_draft and meta_file.is_dir and meta_file.is_overview:
                draft_files[str(Path(path).joinpath(self._meta_plugin_config.dir_meta_file))] = meta_file
        return draft_files

    def _hidden(self, files: bool = False, dirs: bool = False) -> dict[str, MetaFile]:
        """Returns hidden files and/or directories"""

        hidden_files = {}
        for path, meta_file in self.items():
            if meta_file.is_hidden and (
                (files and not dirs and not meta_file.is_dir)
                or (not files and dirs and meta_file.is_dir)
                or (not files and not dirs)
            ):
                hidden_files[path] = meta_file
            elif files and meta_file.is_hidden and meta_file.is_dir and meta_file.is_overview:
                hidden_files[str(Path(path).joinpath(self._meta_plugin_config.dir_meta_file))] = meta_file
        return hidden_files

    @cached_property
    def draft_files(self) -> dict[str, MetaFile]:
        return self._drafts(files=True)

    @cached_property
    def draft_dirs(self) -> dict[str, MetaFile]:
        return self._drafts(dirs=True)

    @cached_property
    def drafts(self) -> dict[str, MetaFile]:
        return self._drafts()

    @cached_property
    def hidden_files(self) -> dict[str, MetaFile]:
        return self._hidden(files=True)

    @cached_property
    def hidden_dirs(self) -> dict[str, MetaFile]:
        return self._hidden(dirs=True)

    @cached_property
    def hidden(self) -> dict[str, MetaFile]:
        return self._hidden()

    def add_meta_files(self, ignored_dirs: list[Path]):
        """Iterate over all files and directories in docs directory"""

        for docs_file in sorted(Path(self._mkdocs_config.docs_dir).rglob("*")):
            meta_link: Optional[MetaFile] = None
            is_ignored = any([docs_file.is_relative_to(ignored_dir) for ignored_dir in ignored_dirs])

            if not is_ignored and docs_file.is_dir():
                meta_link = MetaFile(
                    path=docs_file.relative_to(self._mkdocs_config.docs_dir),
                    abs_path=docs_file,
                    is_dir=True,
                )
            elif (
                not is_ignored
                and docs_file.suffix == ".md"
                and docs_file.name != self._meta_plugin_config.dir_meta_file
            ):
                meta_link = MetaFile(
                    path=docs_file.relative_to(self._mkdocs_config.docs_dir),
                    abs_path=docs_file,
                    is_dir=False,
                )

            if meta_link is not None:
                self[str(meta_link.path)] = meta_link

    def _change_file_slug(self, file: File, file_path: Path):
        # Get URL parts
        if file.url.endswith("/"):
            file.url = file.url[0:-1]
        url_parts = file.url.split("/")

        # Get abs file parts
        path_parts: list[Path] = []
        for path_part in file_path.parts:
            if not path_parts:
                path_parts.append(Path(path_part))
            else:
                path_parts.append(path_parts[-1] / path_part)

        # Replace URL parts that have slug defined
        for position, path_part in enumerate(path_parts):
            meta_file: Optional[MetaFile] = self.get(str(path_part), None)
            if meta_file is not None:
                url_parts[position] = meta_file.slug

        # Recreate file params based on URL with replaced parts
        if file.url != ".":  # Do not modify main index page
            file.url = quote(f"{'/'.join(url_parts)}")
            url_parts.append(file.dest_uri.split("/")[-1])
            if len(url_parts) >= 2 and url_parts[-1] == url_parts[-2]:
                url_parts.pop(-1)
            file.dest_uri = quote("/".join(url_parts))
            if file.dest_uri.endswith("index.html"):
                file.url = f"{file.url}/"
            file.abs_dest_path = str(Path(self._mkdocs_config.site_dir) / file.dest_uri)

    def change_files_slug(self, files: Files, ignored_dirs: list[Path]) -> Files:
        """Change file slug (part of the URL) based of file and parent directories slugs"""

        ignored_dirs.extend([d.abs_path for d in self.draft_files.values()])

        new_files = Files(files=[])
        for file in files:
            file: File
            file_path: Path = Path(file.src_path)
            if (
                (
                    not any([Path(file.abs_src_path).is_relative_to(d) for d in ignored_dirs])
                    and file.src_path not in self.draft_files
                    and str(file_path.name) != self._meta_plugin_config.dir_meta_file
                )
                or (
                    str(file_path.name) == self._meta_plugin_config.dir_meta_file
                    and str(file_path.parent) in self
                    and self[str(file_path.parent)].is_overview
                )
                or (not file.is_documentation_page())
            ):
                if self._meta_plugin_config.slug.enabled:
                    self._change_file_slug(file=file, file_path=file_path)
                new_files.append(file)
            if file.src_path in self:
                self[file.src_path].url = file.url
        return new_files

    def generate_redirect_page(self, file: File) -> Optional[str]:
        """Generates content of redirect page"""

        meta_file: MetaFile = self[file.src_path]
        if meta_file.redirect and not re.search(links.URL_RE_PART, meta_file.redirect):
            log.debug(f"Generating redirect template in file: {meta_file.path}")
            redirect_context = {
                "title": self[str(meta_file.path)].title,
                "url": f"{self._mkdocs_config.site_url}{self[meta_file.redirect].url}",
            }
            return templates.render(tpl_file="redirect.html", context=redirect_context)
        else:
            return None

    def clean_redirect_files(self, files: Files) -> Files:
        """Remove documents that are just redirects to an external URL"""

        new_files = Files(files=[])
        for file in files:
            file: File
            is_redirect_file = False
            if (
                file.src_path in self
                and self[file.src_path].redirect
                and re.search(links.URL_RE_PART, self[file.src_path].redirect)
            ):
                is_redirect_file = True
            if not is_redirect_file:
                new_files.append(file)
            else:
                log.debug(f"Redirects as URL links in file: {file.src_path}")
        return new_files

    def clean_draft_files(self, files: Files) -> Files:
        new_files = Files(files=[])
        for file in files:
            if file.src_path not in self.draft_files:
                new_files.append(file)
            else:
                log.debug(f"Removed draft file: {file.src_path}")
        return new_files

    def files_gen(self) -> Generator[MetaFile, Any, None]:
        """Meta files generator used for building navigation"""
        for meta_file in self.values():
            meta_file: MetaFile
            yield meta_file
