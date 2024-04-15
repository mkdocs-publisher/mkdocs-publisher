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
from dataclasses import dataclass
from hashlib import md5
from pathlib import Path
from typing import Optional

log = logging.getLogger("mkdocs.plugins.publisher._shared.links")


ANCHOR_RE_PART = r"((#(?P<anchor>([^|\][()'\"]+)))?)"
EXTRA_RE_PART = r"( *({(?P<extra>[\w+=. ]+)})?)"
IMAGE_RE_PART = r"((\|(?P<image>([0-9x]+)))?)"
LINK_RE_PART = r"(?P<link>(?!(https?|ftp)://)[^|#()\r\n\t\f\v]+)"
URL_RE_PART = r"(?P<link>((https?|ftp)://)?[\w\-]{2,}\.[\w\-]{2,}(\.[\w\-]{2,})?([^\s\][)(]*))"
TEXT_RE_PART = r"(?P<text>[^\][)(|]+)"
LINK_TITLE_RE_PART = r"(( \"(?P<title>[ \S]+)\")?)"

HTTP_LINK_RE = re.compile(rf"\[{TEXT_RE_PART}]\({URL_RE_PART}\)")
WIKI_LINK_RE = re.compile(rf"(?<!!)\[\[{LINK_RE_PART}{ANCHOR_RE_PART}(\|{TEXT_RE_PART})?]]")
WIKI_EMBED_LINK_RE = re.compile(
    rf"!\[\[{LINK_RE_PART}{ANCHOR_RE_PART}{IMAGE_RE_PART}]]{EXTRA_RE_PART}"
)
MD_LINK_RE = re.compile(
    rf"(?<!!)\[{TEXT_RE_PART}]\({LINK_RE_PART}{ANCHOR_RE_PART}"
    rf"{LINK_TITLE_RE_PART}\){EXTRA_RE_PART}"
)
MD_EMBED_LINK_RE = re.compile(
    rf"!\[{TEXT_RE_PART}]\({LINK_RE_PART}{LINK_TITLE_RE_PART}\){EXTRA_RE_PART}"
)
RELATIVE_LINK_RE = re.compile(
    rf"\[{TEXT_RE_PART}]\({LINK_RE_PART}{ANCHOR_RE_PART}{LINK_TITLE_RE_PART}\)"
)
ANCHOR_LINK_RE = re.compile(rf"(?<!!)\[{TEXT_RE_PART}]\({ANCHOR_RE_PART}{LINK_TITLE_RE_PART}\)")


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
    text: Optional[str]
    anchor: Optional[str]
    extra: Optional[str] = None
    link: Optional[str] = None
    title: Optional[str] = None
    is_wiki: bool = False

    def __repr__(self):
        anchor = f"#{self.anchor}" if self.anchor else ""
        extra: list = self.extra.strip().split(" ") if self.extra else []
        title = f' "{self.title}"' if self.title else ""

        if self.is_wiki:
            if self.text is None and self.anchor:
                self.text = f"{self.link} > {self.anchor}"
            elif self.text is None:
                self.text = self.link
            link = f"{self.link}.md" if self.link else ""
        else:
            link = self.link if self.link else ""

        link_extra = f'{{{" ".join(extra)}}}' if extra else ""
        final_link = f"[{self.text}]({link}{anchor}{title}){link_extra}"
        log.debug(final_link)
        return final_link

    @property
    def backlink_anchor(self):
        return f"#{md5(self.link.encode()).hexdigest()}"

    @property
    def as_backlink(self):
        anchor = f"#{self.anchor}" if self.anchor else ""
        extra: list = self.extra.strip().split(" ") if self.extra else []
        extra.append(self.backlink_anchor)
        title = f' "{self.title}"' if self.title else ""
        link = self.link if self.link else ""

        link_extra = f'{{{" ".join(extra)}}}' if extra else ""
        final_link = f"[{self.text}]({link}{anchor}{title}){link_extra}"
        log.debug(final_link)
        return final_link


@dataclass
class WikiEmbedLinkMatch:
    link: str
    image: Optional[str]
    anchor: Optional[str]
    extra: Optional[str]

    def __repr__(self):
        extra: list = self.extra.strip().split(" ") if self.extra else []

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
        final_link = f"![{self.link.split('/')[-1]}]({self.link}){link_extra}"
        log.debug(final_link)
        return final_link


@dataclass
class MdEmbedLinkMatch:
    link: str
    text: str
    extra: Optional[str]
    title: Optional[str]
    is_loading_lazy: bool = True

    def __repr__(self):
        extra: list = self.extra.strip().split(" ") if self.extra else []
        title = f' "{self.title}"' if self.title else ""

        if self.is_loading_lazy and "loading=lazy" not in extra:
            extra.append("loading=lazy")
        link_extra = f'{{{" ".join(extra)}}}' if extra else ""
        final_link = f"![{self.text}]({self.link}{title}){link_extra}"
        log.debug(final_link)
        return final_link


@dataclass
class RelativeLinkMatch:
    link: str
    text: str
    anchor: Optional[str]
    title: Optional[str]
    relative_path_finder: Optional[RelativePathFinder] = None

    def __repr__(self):
        anchor = f"#{self.anchor}" if self.anchor else ""
        title = f' "{self.title}"' if self.title else ""

        # The same page anchor link doesn't have file part
        if self.link.startswith("#"):
            final_link = f"[{self.text}]({self.link})"
            log.debug(final_link)
            return final_link

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
        final_link = f"[{self.text}]({link}{anchor}{title})"
        log.debug(final_link)
        return final_link
