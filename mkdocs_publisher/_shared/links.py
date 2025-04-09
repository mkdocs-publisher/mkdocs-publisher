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

# MIT License
#
# Copyright (c) 2023-2025 Maciej 'maQ' Kusz <maciej.kusz@gmail.com>
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
import re
import urllib.parse
from dataclasses import dataclass
from dataclasses import field
from hashlib import md5
from pathlib import Path

import pymdownx.slugs

from mkdocs_publisher._shared.config_enums import SlugModeChoiceEnum

log = logging.getLogger("mkdocs.publisher._shared.links")


ANCHOR_RE_PART = r"((#(?P<anchor>([^|\][()'\"]+)))?)"
EXTRA_RE_PART = r"(( ?{(?P<extra>[\w\d\S ]+)})?)"
IMAGE_RE_PART = r"((\|(?P<image>([0-9x]+)))?)"
LINK_RE_PART = r"(?P<link>(?!(https?|ftp)://)[^|#()\r\n\t\f\v]+)"
URL_RE_PART = r"(?P<link>((https?|ftp)://)[\w\-]{2,}\.[\w\-]{2,}(\.[\w\-]{2,})?([^\s\][)(]*))"
TEXT_RE_PART = r"(?P<text>[^\][|]+)"
LINK_TITLE_RE_PART = r"(( \"(?P<title>[ \S]+)\")?)"

HTTP_LINK_RE = re.compile(rf"\[{TEXT_RE_PART}]\({URL_RE_PART}\)")
WIKI_LINK_RE = re.compile(rf"(?<!!)\[\[({LINK_RE_PART}?){ANCHOR_RE_PART}(\|{TEXT_RE_PART})?]]{EXTRA_RE_PART}")
WIKI_EMBED_LINK_RE = re.compile(rf"!\[\[{LINK_RE_PART}{ANCHOR_RE_PART}{IMAGE_RE_PART}]]{EXTRA_RE_PART}")
MD_LINK_RE = re.compile(
    rf"(?<!!)\[{TEXT_RE_PART}]\({LINK_RE_PART}{ANCHOR_RE_PART}{LINK_TITLE_RE_PART}\){EXTRA_RE_PART}",
)
MD_EMBED_LINK_RE = re.compile(rf"!\[{TEXT_RE_PART}]\({LINK_RE_PART}{LINK_TITLE_RE_PART}\){EXTRA_RE_PART}")
RELATIVE_LINK_RE = re.compile(rf"\[{TEXT_RE_PART}?]\({LINK_RE_PART}{ANCHOR_RE_PART}{LINK_TITLE_RE_PART}\)")
ANCHOR_LINK_RE = re.compile(rf"(?<!!)\[{TEXT_RE_PART}]\({ANCHOR_RE_PART}{LINK_TITLE_RE_PART}\)")


def slugify(text: str) -> str:
    """Text slugify function that produces the same slug as MkDocs one"""
    text = urllib.parse.unquote(text)
    text = pymdownx.slugs.slugify(case="lower", normalize="NFD")(text=text, sep="-")
    return str(text).encode("ASCII", "ignore").decode("utf-8")


def create_slug(
    file_name: str,
    slug_mode: SlugModeChoiceEnum | str,
    slug: str | None,
    title: str | None,
    warn_on_missing: bool = True,
) -> str | None:
    """Generate slug for various modes"""
    # When slug from meta key is not present, try to get slug value the other way
    if slug is None or slug == "none":
        if slug_mode == SlugModeChoiceEnum.TITLE and title is not None:
            slug = slugify(text=title)
        elif slug_mode == SlugModeChoiceEnum.FILENAME:
            slug = slugify(text=file_name)

    # Log slug value
    if slug is None or slug == "none":
        slug = slugify(text=file_name)

        if warn_on_missing:
            log.warning(f'No slug for file "{file_name}" (mode: {slug_mode}). Fallback to file name.')

    log.debug(f'Slug for file "{file_name}" is: "{slug}"')
    return slug


class RelativePathFinder:
    def __init__(self, current_file_path: Path, docs_dir: Path, blog_dir: Path | None, relative_path: Path) -> None:
        self._current_file_path: Path = current_file_path
        self._docs_dir: Path = docs_dir
        self._blog_dir: Path | None = blog_dir
        self._relative_path: Path = relative_path

    @property
    def current_file_path(self) -> Path:
        return self._current_file_path

    @property
    def relative_path(self) -> Path:
        return self._relative_path

    def get_full_file_path(self, file_path: Path) -> Path | None:
        """Find full file path."""
        full_file_path = self._docs_dir / file_path
        log.debug(f"Looking for file: {full_file_path!s}")
        if not full_file_path.is_file():
            # Build list of unique found files paths
            found_files_list: list[Path] = []
            for f in self._docs_dir.glob(f"**/{file_path}"):
                f = f.resolve(strict=True)
                if f not in found_files_list:  # pragma: no cover
                    found_files_list.append(f)

            # Remove blog duplicates (generated during build process)
            if len(found_files_list) == 2 and self._blog_dir:
                blog_dir = self._docs_dir.joinpath(self._blog_dir)
                found_files_list = [f for f in found_files_list if not f.is_relative_to(blog_dir)]

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
                    f"{[str(f.relative_to(self._docs_dir)) for f in found_files_list]} "
                    f"for link in file: {full_file_path!s}",
                )
                full_file_path = None
        return full_file_path

    def get_relative_file_path(self, file_path: Path | None) -> str | None:
        """Get file path relative to currently opened file."""
        if file_path is not None:
            current_file_parts = list(Path(self._current_file_path).parts)
            current_file_parts[0] = str(self._relative_path)
            found_file_parts = list(file_path.relative_to(self._docs_dir).parts)
            relative_file_parts = []
            relative_file_missing_pieces = found_file_parts[:]

            index = 0
            for index, part in enumerate(current_file_parts[:-1]):
                if index < len(found_file_parts):
                    if part == found_file_parts[index]:
                        del relative_file_missing_pieces[0]
                    else:
                        relative_file_parts.append("..")
                else:
                    relative_file_parts.append("..")
                    relative_file_parts.extend(relative_file_missing_pieces)
            if index < len(found_file_parts):
                relative_file_parts.extend(relative_file_missing_pieces)
            return str(Path(*relative_file_parts))
        return None


@dataclass(kw_only=True)
class _LinksCommon:
    anchor: str | None = None
    extra: str | None = None
    title: str | None = None
    _anchor: str = field(init=False, repr=False, compare=False, default="")
    _extra_list: list[str] = field(init=False, repr=False, compare=False, default_factory=list)
    _title: str = field(init=False, repr=False, compare=False, default="")

    def __post_init__(self):  # noqa: ANN204
        self._anchor = f"#{slugify(self.anchor)}" if self.anchor else ""
        self._extra_list = self.extra.strip().split(" ") if self.extra else []
        self._title = f' "{self.title}"' if self.title else ""

    @property
    def _extra(self) -> str:
        return f'{{ {" ".join(self._extra_list)} }}' if self._extra_list else ""


@dataclass(kw_only=True)
class LinkMatch(_LinksCommon):
    text: str | None
    link: str | None = None
    is_wiki: bool = False

    def __repr__(self) -> str:
        if self.is_wiki:
            if self.text is None and self.link is not None and self.anchor:
                self.text = f"{self.link} > {self.anchor}"
            elif self.text is None and self.anchor:
                self.text = self.anchor
            elif self.text is None:
                self.text = self.link
            link = f"{self.link}.md" if self.link else ""
        else:
            link = self.link if self.link else ""

        final_link = f"[{self.text}]({link}{self._anchor}{self._title}){self._extra}"
        log.debug(final_link)
        return final_link

    @property
    def backlink_anchor(self) -> str:
        return f"#{md5(self.link.encode()).hexdigest()}"  # noqa: S324

    @property
    def as_backlink(self) -> str:
        self._extra_list.append(self.backlink_anchor)
        title = f' "{self.title}"' if self.title else ""
        link = self.link if self.link else ""

        final_link = f"[{self.text}]({link}{self._anchor}{title}){self._extra}"
        log.debug(final_link)
        return final_link


@dataclass(kw_only=True)
class WikiEmbedLinkMatch(_LinksCommon):
    image: str | None
    link: str

    def __repr__(self) -> str:
        if self.image:
            try:
                width, height = self.image.split("x")
            except ValueError:
                width = self.image
                height = None
            self._extra_list.append(f"width={width}")
            if height:
                self._extra_list.append(f"height={height}")

        if str(self.link).lower().endswith(".pdf"):
            self._extra_list.append("pdfjs")
            if self.anchor:
                self._extra_list.append(self.anchor)
            self.anchor = None

        final_link = f"![{self.link.split('/')[-1]}]({self.link}){self._extra}"
        log.debug(final_link)
        return final_link


@dataclass(kw_only=True)
class MdEmbedLinkMatch(_LinksCommon):
    link: str
    text: str
    is_loading_lazy: bool = True

    def __repr__(self) -> str:
        if self.is_loading_lazy and "loading=lazy" not in self._extra_list:
            self._extra_list.append("loading=lazy")
        final_link = f"![{self.text}]({self.link}{self._title}){self._extra}"
        log.debug(final_link)
        return final_link


@dataclass(kw_only=True)
class RelativeLinkMatch(_LinksCommon):
    link: str
    text: str
    relative_path_finder: RelativePathFinder | None = None

    def __repr__(self) -> str:
        # On the same page anchor link doesn't have file part
        if self.link.startswith("#"):
            final_link = f"[{self.text}]({self.link})"
        else:
            # Link from blog sub-pages have to be recalculated for a new relative value
            if (
                str(self.relative_path_finder.current_file_path).startswith(
                    str(self.relative_path_finder.relative_path),
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
            final_link = f"[{self.text}]({link}{self._anchor}{self._title})"
        log.debug(final_link)
        return final_link
