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
import re
from dataclasses import dataclass
from typing import cast

from mkdocs.config.defaults import MkDocsConfig
from mkdocs.structure.pages import Page

from mkdocs_publisher._shared import links
from mkdocs_publisher.blog.plugin import BlogPlugin

log = logging.getLogger("mkdocs.publisher.obsidian.backlinks")


@dataclass
class Link:
    text: str
    destination: str
    title: str
    source: str


class BacklinkLinks:
    def __init__(
        self,
        mkdocs_config: MkDocsConfig,
        backlinks: dict[str, list[Link]],
    ):
        self._mkdocs_config: MkDocsConfig = mkdocs_config
        self._backlinks: dict[str, list[Link]] = backlinks

    @staticmethod
    def _other_link_to_text(match: re.Match) -> str:
        """Return only a text from a link (http or markdown)"""
        return match.groupdict()["link"]

    @staticmethod
    def _create_backlink(match: re.Match):
        link = links.LinkMatch(**match.groupdict())
        return link.as_backlink

    def _parse_markdown_link(self, match: re.Match, page: Page, line: str):
        """Parse markdown link"""
        original_link = links.LinkMatch(**match.groupdict())
        backlink_link = f"{self._mkdocs_config.site_url}{page.url}{original_link.backlink_anchor}"

        # Convert document link into backlink
        link_replacement = f'<a href="{backlink_link}">{original_link.text}</a>'
        backlink_text = line.replace(str(original_link), link_replacement)

        # Convert other links into text
        backlink_text = re.sub(links.MD_LINK_RE, self._other_link_to_text, backlink_text)
        backlink_text = re.sub(links.HTTP_LINK_RE, self._other_link_to_text, backlink_text)

        # Create a backlink with context
        backlink_text = f'<p class="obsidian_backlink">{backlink_text}</p>'

        # Convert relative backlinks into absolute backlinks inside document directory
        original_link_source = page.file.src_uri
        if len(original_link.link.split("/")) == 1:
            destination_pre = original_link_source.split("/")[:-1]
            destination_pre.append(str(original_link.link))
            original_link.link = "/".join(destination_pre)
        original_link.link = original_link.link.replace("../", "")

        new_link = Link(
            text=backlink_text,
            destination=backlink_link,
            source=original_link.link,
            title=str(page.title),
        )

        # Get blog temporary files
        temp_blog_files = []
        if "pub-blog" in self._mkdocs_config.plugins:
            blog_plugin: BlogPlugin = cast(BlogPlugin, self._mkdocs_config.plugins["pub-blog"])
            temp_blog_files = blog_plugin.blog_config.temp_files_list

        # Do not add backlink if backlinks points to the same document
        if original_link_source != original_link.link and original_link_source not in temp_blog_files:
            log.debug(
                f"Found backlink to: {original_link.link}"
                f"{original_link.anchor if original_link.anchor is not None else ''}"
            )
            if original_link.link not in self._backlinks:
                self._backlinks[original_link.link] = [new_link]
            else:
                link_found = False
                for existing_link in self._backlinks[original_link.link]:
                    # Add backlink to an existing one
                    if existing_link.title == new_link.title:
                        link_found = True
                        existing_link.text = f"{existing_link.text}<hr>{new_link.text}"
                if not link_found:
                    self._backlinks[original_link.link].append(new_link)

    def find_markdown_links(self, markdown: str, page: Page):
        # """Find all markdown backlinks"""
        for line in markdown.split("\n"):
            for match in re.finditer(links.MD_LINK_RE, line):
                self._parse_markdown_link(match=match, page=page, line=line)

    def convert_to_backlink(self, markdown: str) -> str:
        """Convert backlink to link with an anchor for direct navigation after clicking on it"""
        return re.sub(links.MD_LINK_RE, self._create_backlink, markdown)
