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
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Optional
from typing import cast

from mkdocs.config.defaults import MkDocsConfig

# noinspection PyProtectedMember
from mkdocs_publisher._shared import mkdocs_utils

# noinspection PyProtectedMember
from mkdocs_publisher._shared.urls import slugify
from mkdocs_publisher.blog.config import BlogPluginConfig
from mkdocs_publisher.obsidian.config import _ObsidianLinksConfig

log = logging.getLogger("mkdocs.plugins.publisher.obsidian.md_links")

ANCHOR_RE_PART = r"((#(?P<anchor>([^|\][()]+)))?)"
EXTRA_RE_PART = r"( *({(?P<extra>[\w+=. ]+)})?)"
IMAGE_RE_PART = r"((\|(?P<image>([0-9x]+)))?)"
LINK_RE_PART = r"(?P<link>(?!https?://)[^#()\s]+)"
TEXT_RE_PART = r"(?P<text>[ \S]+)"

WIKI_LINK_RE = re.compile(rf"(?<!!)\[\[(?P<link>[^#()\s]+){ANCHOR_RE_PART}[|]{TEXT_RE_PART}]]")
WIKI_EMBED_LINK_RE = re.compile(
    rf"!\[\[{LINK_RE_PART}{ANCHOR_RE_PART}{IMAGE_RE_PART}]]{EXTRA_RE_PART}"
)
MD_LINK_RE = re.compile(rf"(?<!!)\[{TEXT_RE_PART}]\({LINK_RE_PART}{ANCHOR_RE_PART}\)")
MD_EMBED_LINK_RE = re.compile(rf"!\[{TEXT_RE_PART}]\({LINK_RE_PART}\){EXTRA_RE_PART}")
RELATIVE_LINK_RE = re.compile(rf"\[{TEXT_RE_PART}]\({LINK_RE_PART}{ANCHOR_RE_PART}\)")


class RelativePathFinder:
    def __init__(self, current_file_path: Path, docs_dir: Path, relative_path: Path):
        self._current_file_path: Path = current_file_path
        self._docs_dir: Path = docs_dir
        self._relative_path: Path = relative_path

    @property
    def current_file_path(self) -> Path:
        return self._current_file_path

    @property
    def relative_path(self) -> Path:
        return self._relative_path

    def get_full_file_path(self, file_path: Path) -> Optional[Path]:
        """Find full file path."""
        full_file_path = self._docs_dir / file_path
        log.debug(f"Looking for file: {str(full_file_path)}")
        if not full_file_path.is_file():
            # Build list of unique found files paths
            found_files_list: list[Path] = []
            for f in self._docs_dir.glob(f"**/{file_path}"):
                f = f.resolve(strict=True)
                if f not in found_files_list:  # pragma: no cover
                    found_files_list.append(f)
            # Check how many files were found (there should be only one)
            no_of_found_files = len(found_files_list)
            if no_of_found_files == 1:
                full_file_path = found_files_list[0]
                log.debug(f'File: "{file_path} found: "{full_file_path}"')
            elif no_of_found_files <= 0:
                log.error(f'File: "{file_path}" doesn\'t exists (from: "{self._docs_dir}")')
                full_file_path = None
            else:
                log.error(
                    f"Too much files found: "
                    f"{[str(f.relative_to(self._docs_dir)) for f in found_files_list]}"
                )
                full_file_path = None
        return full_file_path

    def get_relative_file_path(self, file_path: Path) -> Path:
        """Get file path relative to currently opened file."""
        current_file_parts = list(Path(self._current_file_path).parts)
        current_file_parts[0] = str(self._relative_path)
        found_file_parts = list(file_path.relative_to(self._docs_dir).parts)
        relative_file_parts = []
        relative_file_missing_pieces = found_file_parts[:]
        index = 0
        for index, part in enumerate(current_file_parts[:-1]):
            try:
                if part == found_file_parts[index]:
                    del relative_file_missing_pieces[0]
                else:
                    relative_file_parts.append("..")
            except IndexError:
                relative_file_parts.append("..")
                relative_file_parts.extend(relative_file_missing_pieces)
        if index < len(found_file_parts):
            relative_file_parts.extend(relative_file_missing_pieces)
        return Path(*relative_file_parts)


@dataclass
class LinkMatch:
    link: str
    text: str
    anchor: Optional[str]
    is_wiki: bool = False

    def __repr__(self):
        if self.anchor:
            anchor = f"#{slugify(text=self.anchor)}"
        else:
            anchor = ""
        if self.is_wiki:
            link = f"{self.link}.md"
        else:
            link = self.link
        return f"[{self.text}]({link}{anchor})"


@dataclass
class WikiEmbedLinkMatch:
    link: str
    image: Optional[str]
    anchor: Optional[str]
    extra: Optional[str]

    def __repr__(self):
        if self.extra:
            extra: list = self.extra.strip().split(" ")
        else:
            extra = []
        if self.image:
            try:
                width, height = self.image.split("x")
            except ValueError:
                width = self.image
                height = None
            extra.append(f"width={width}")
            if height:
                extra.append(f"height={height}")
        if str(self.link).lower().endswith(".pdf"):
            extra.append("pdfjs")
            if self.anchor:
                extra.append(self.anchor)
            self.anchor = None
        link_extra = f'{{{" ".join(extra)}}}' if extra else ""
        return f"![{self.link.split('/')[-1]}]({self.link}){link_extra}"


@dataclass
class MdEmbedLinkMatch:
    link: str
    text: str
    extra: Optional[str]
    is_loading_lazy: bool = True

    def __repr__(self):
        if self.extra:
            extra: list = self.extra.strip().split(" ")
        else:
            extra = []
        if self.is_loading_lazy and "loading=lazy" not in extra:
            extra.append("loading=lazy")
        if extra:
            link_extra = f'{{{" ".join(extra)}}}'
        else:
            link_extra = ""
        return f"![{self.text}]({self.link}){link_extra}"


@dataclass
class RelativeLinkMatch:
    link: str
    text: str
    anchor: Optional[str]
    relative_path_finder: Optional[RelativePathFinder] = None

    def __repr__(self):
        if self.anchor:
            anchor = f"#{slugify(text=self.anchor)}"
        else:
            anchor = ""
        # The same page anchor link doesn't have file part
        if self.link.startswith("#"):
            return f"[{self.text}]({self.link})"
        # Link from blog sub pages have to be recalculated for a new relative value
        if (
            str(self.relative_path_finder.current_file_path).startswith(
                str(self.relative_path_finder.relative_path)
            )
            or str(self.relative_path_finder.current_file_path).startswith("index-")
        ) and (
            # TODO: rethink RSS file filtering
            not self.link.endswith(".xml")  # RSS feed exclusion
        ):
            file_path = self.relative_path_finder.get_full_file_path(file_path=Path(self.link))
            if file_path is not None:
                link = str(self.relative_path_finder.get_relative_file_path(file_path=file_path))
            else:
                link = ""
        else:
            link = self.link
        return f"[{self.text}]({link}{anchor})"


class MarkdownLinks:
    def __init__(self, mkdocs_config: MkDocsConfig):
        self._current_file_path: Optional[str] = None
        self._mkdocs_config: MkDocsConfig = mkdocs_config
        self._links_config: _ObsidianLinksConfig = mkdocs_config.plugins[
            "pub-obsidian"
        ].config.links
        self._blog_config: Optional[BlogPluginConfig] = mkdocs_utils.get_plugin_config(
            mkdocs_config=mkdocs_config, plugin_name="pub-blog"
        )  # type: ignore

    @staticmethod
    def _normalize_wiki_embed_link(match: re.Match) -> str:
        wiki_embed_link = str(WikiEmbedLinkMatch(**match.groupdict()))
        log.debug(f"Normalizing wiki embed link: {match.group(0)} > {wiki_embed_link}")
        return wiki_embed_link

    @staticmethod
    def _normalize_wiki_link(match: re.Match) -> str:
        wiki_link_obj = LinkMatch(**match.groupdict())
        wiki_link_obj.is_wiki = True
        wiki_link = str(wiki_link_obj)
        log.debug(f"Normalizing wiki link: {match.group(0)} > {wiki_link}")
        return wiki_link

    def _normalize_md_embed_link(self, match: re.Match) -> str:
        md_embed_link_obj = MdEmbedLinkMatch(**match.groupdict())
        md_embed_link_obj.is_loading_lazy = self._links_config.img_lazy_loading
        md_embed_link = str(md_embed_link_obj)
        log.debug(f"Normalizing md embed link: {match.group(0)} > {md_embed_link}")
        return md_embed_link

    @staticmethod
    def _normalize_md_links(match: re.Match) -> str:
        md_link = str(LinkMatch(**match.groupdict()))
        log.debug(f"Normalizing md link: {match.group(0)} > {md_link}")
        return md_link

    def normalize_links(self, markdown: str, current_file_path: str) -> str:
        self._current_file_path = current_file_path
        if self._links_config.wikilinks_enabled:
            markdown = re.sub(WIKI_LINK_RE, self._normalize_wiki_link, markdown)
            markdown = re.sub(WIKI_EMBED_LINK_RE, self._normalize_wiki_embed_link, markdown)
        markdown = re.sub(MD_EMBED_LINK_RE, self._normalize_md_embed_link, markdown)
        markdown = re.sub(MD_LINK_RE, self._normalize_md_links, markdown)
        return markdown

    def _normalize_relative_link(self, match: re.Match) -> str:
        md_link_obj = RelativeLinkMatch(**match.groupdict())
        md_link_obj.relative_path_finder = RelativePathFinder(
            current_file_path=Path(cast(str, self._current_file_path)),
            docs_dir=Path(self._mkdocs_config.docs_dir),
            relative_path=Path(cast(str, self._blog_config.blog_dir)),
        )
        return str(md_link_obj)

    def normalize_relative_links(self, markdown: str, current_file_path: str) -> str:
        self._current_file_path = current_file_path
        markdown = re.sub(RELATIVE_LINK_RE, self._normalize_relative_link, markdown)
        return markdown
