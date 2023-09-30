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
from pathlib import Path
from typing import Optional
from typing import cast

from mkdocs.config.defaults import MkDocsConfig

# noinspection PyProtectedMember
from mkdocs_publisher._shared import links
from mkdocs_publisher._shared import mkdocs_utils

# noinspection PyProtectedMember
from mkdocs_publisher.blog.config import BlogPluginConfig
from mkdocs_publisher.obsidian.config import _ObsidianLinksConfig

log = logging.getLogger("mkdocs.plugins.publisher.obsidian.md_links")


class MarkdownLinks:
    def __init__(self, mkdocs_config: MkDocsConfig):
        self._current_file_path: Optional[str] = None
        self._mkdocs_config: MkDocsConfig = mkdocs_config
        self._links_config: _ObsidianLinksConfig = mkdocs_config.plugins[
            "pub-obsidian"
        ].config.links
        self._blog_config: Optional[BlogPluginConfig] = cast(
            BlogPluginConfig,
            mkdocs_utils.get_plugin_config(mkdocs_config=mkdocs_config, plugin_name="pub-blog"),
        )

    @staticmethod
    def _normalize_wiki_embed_link(match: re.Match) -> str:
        wiki_embed_link = str(links.WikiEmbedLinkMatch(**match.groupdict()))
        log.debug(f"Normalizing wiki embed link: {match.group(0)} > {wiki_embed_link}")
        return wiki_embed_link

    @staticmethod
    def _normalize_wiki_link(match: re.Match) -> str:
        wiki_link_obj = links.LinkMatch(**match.groupdict())
        wiki_link_obj.is_wiki = True
        wiki_link = str(wiki_link_obj)
        log.debug(f"Normalizing wiki link: {match.group(0)} > {wiki_link}")
        return wiki_link

    def _normalize_md_embed_link(self, match: re.Match) -> str:
        md_embed_link_obj = links.MdEmbedLinkMatch(**match.groupdict())
        md_embed_link_obj.is_loading_lazy = self._links_config.img_lazy_loading
        md_embed_link = str(md_embed_link_obj)
        log.debug(f"Normalizing md embed link: {match.group(0)} > {md_embed_link}")
        return md_embed_link

    @staticmethod
    def _normalize_md_links(match: re.Match) -> str:
        md_link = str(links.LinkMatch(**match.groupdict()))
        log.debug(f"Normalizing md link: {match.group(0)} > {md_link}")
        return md_link

    def normalize_links(self, markdown: str, current_file_path: str) -> str:
        self._current_file_path = current_file_path
        if self._links_config.wikilinks_enabled:
            markdown = re.sub(links.WIKI_LINK_RE, self._normalize_wiki_link, markdown)
            markdown = re.sub(links.WIKI_EMBED_LINK_RE, self._normalize_wiki_embed_link, markdown)
        markdown = re.sub(links.MD_EMBED_LINK_RE, self._normalize_md_embed_link, markdown)
        markdown = re.sub(links.MD_LINK_RE, self._normalize_md_links, markdown)
        return markdown

    def _normalize_relative_link(self, match: re.Match) -> str:
        md_link_obj = links.RelativeLinkMatch(**match.groupdict())
        md_link_obj.relative_path_finder = links.RelativePathFinder(
            current_file_path=Path(cast(str, self._current_file_path)),
            docs_dir=Path(self._mkdocs_config.docs_dir),
            relative_path=Path(cast(str, self._blog_config.blog_dir)),
        )
        return str(md_link_obj)

    def normalize_relative_links(self, markdown: str, current_file_path: str) -> str:
        self._current_file_path = current_file_path
        markdown = re.sub(links.RELATIVE_LINK_RE, self._normalize_relative_link, markdown)
        return markdown
