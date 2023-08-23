import logging
import re
from pathlib import Path
from typing import Optional

from mkdocs.config.defaults import MkDocsConfig

# noinspection PyProtectedMember
from mkdocs_publisher._shared import mkdocs_utils

# noinspection PyProtectedMember
from mkdocs_publisher._shared.urls import slugify
from mkdocs_publisher.blog.config import BlogPluginConfig
from mkdocs_publisher.obsidian.config import _ObsidianLinksConfig

log = logging.getLogger("mkdocs.plugins.publisher.obsidian.md_links")


WIKI_LINK_RE = re.compile(r"(?<!!)\[\[(\S+[|[ \S]+]*)]]")
WIKI_LINK_EMBED_RE = re.compile(r"!\[\[(\S+[|[ \S]+]*)]]")
MARKDOWN_LINK_RE = re.compile(r"(?<!!)\[([^][\r\n]+)]\(((?!https?://)[^][)(\s]?)(#[\w\S]+)?\)")
MARKDOWN_LINK_EMBED_RE = re.compile(r"!\[([^][\r\n]+)]\(((?!https?://)[^][)(\s]+)\)")
MARKDOWN_FILE_RE = re.compile(r"\[([^][\r\n]+)]\(((?!https?://)[^][)(\s]+.md)(#[\w\S]+)?\)")


class MarkdownLinks:
    def __init__(self, mkdocs_config: MkDocsConfig, disable_lazy_loading_override: bool = False):
        self._mkdocs_config: MkDocsConfig = mkdocs_config
        self._links_config: _ObsidianLinksConfig = mkdocs_config.plugins[
            "pub-obsidian"
        ].config.links
        self._current_file_path: Optional[str] = None
        self._disable_lazy_loading_override: bool = disable_lazy_loading_override
        self._blog_config: Optional[BlogPluginConfig] = mkdocs_utils.get_plugin_config(
            mkdocs_config=mkdocs_config, plugin_name="pub-blog"
        )  # type: ignore

    def _parse_wiki_link(self, link: str) -> tuple[str, str]:
        if "|" in link:
            try:
                link, name = link.split("|")
            except ValueError:
                log.warning(f'Error in link: {link} (from: "{self._current_file_path}")')
                return "", ""
        else:
            name = link.split("/")[-1]
        return link, name

    def _get_file_path(self, file_path: str) -> str:

        file_path = file_path.replace("../", "")
        full_file_path = Path(self._mkdocs_config.docs_dir) / file_path
        if not full_file_path.exists():
            found_files_list: list[Path] = [
                f for f in Path(self._mkdocs_config.docs_dir).glob(f"**/{file_path}")
            ]
            for found_file in found_files_list:
                if found_file.resolve().exists():
                    full_file_path = found_file
                    break
            else:
                log.warning(
                    f'File: "{full_file_path}" doesn\'t exists (from: "{self._current_file_path}")'
                )
                return ""

        return f"/{full_file_path.relative_to(self._mkdocs_config.docs_dir)}"

    def _normalize_wiki_link_embed(self, match: re.Match) -> str:
        link, name = self._parse_wiki_link(link=match.group(1))

        # TODO: parse from 'name' variable image size, etc.
        # (https://help.obsidian.md/Linking+notes+and+files/Embedding+files)

        link = self._get_file_path(link)
        link = f"![{name}]({link})"
        return link

    def _normalize_wiki_link(self, match: re.Match) -> str:
        link, name = self._parse_wiki_link(link=match.group(1))
        link = self._get_file_path(f"{link}.md")
        link = f"[{name}]({link})"
        return link

    def _normalize_markdown_link_embed(self, match: re.Match) -> str:
        name = match.group(1)
        link = f"![{name}]({self._get_file_path(match.group(2))})"
        if self._links_config.img_lazy_loading and not self._disable_lazy_loading_override:
            link = f"{link}{{ loading=lazy }}"
        return link

    def _fix_relative_path(self, match: re.Match) -> str:
        """Fix relative links in dynamically created documents
        like categories, tags and post previews"""
        anchor_link = f"#{slugify(text=match.group(3))}" if match.group(3) is not None else ""
        link = self._get_file_path(file_path=match.group(2))
        link = f"[{match.group(1)}]({link}{anchor_link})"
        return link

    @staticmethod
    def _fix_anchor_links(match: re.Match) -> str:
        anchor_link = f"#{slugify(text=match.group(3))}" if match.group(3) is not None else ""
        link = f"[{match.group(1)}]({match.group(2)}{anchor_link})"
        return link

    def normalize(self, markdown: str, file_path: str) -> str:
        self._current_file_path = file_path
        if self._links_config.wikilinks_enabled:
            markdown = re.sub(WIKI_LINK_RE, self._normalize_wiki_link, markdown)
            markdown = re.sub(WIKI_LINK_EMBED_RE, self._normalize_wiki_link_embed, markdown)
        markdown = re.sub(MARKDOWN_LINK_EMBED_RE, self._normalize_markdown_link_embed, markdown)
        markdown = re.sub(MARKDOWN_LINK_RE, self._fix_anchor_links, markdown)
        return markdown

    def fix_relative_paths(self, markdown: str) -> str:
        markdown = re.sub(MARKDOWN_FILE_RE, self._fix_relative_path, markdown)
        return markdown

    def _fix_blog_sub_paths(self, match: re.Match) -> str:
        # TODO: remove this method when rewriting blog engine
        link = self._get_file_path(file_path=match.group(2))
        anchor_link = f"#{slugify(text=match.group(3))}" if match.group(3) is not None else ""
        link = f"[{match.group(1)}](../..{link}{anchor_link})"
        return link

    def _fix_blog_main_paths(self, match: re.Match) -> str:
        # TODO: remove this method when rewriting blog engine
        link = self._get_file_path(file_path=match.group(2))
        anchor_link = f"#{slugify(text=match.group(3))}" if match.group(3) is not None else ""
        link = f"[{match.group(1)}]({link[1:]}{anchor_link})"
        return link

    def fix_blog_paths(self, markdown: str, source_file: Path) -> str:
        # TODO: remove this method when rewriting blog engine
        if str(source_file).startswith(f"{self._blog_config.temp_dir}/{self._blog_config.slug}"):
            markdown = re.sub(MARKDOWN_FILE_RE, self._fix_blog_sub_paths, markdown)
        elif str(source_file).startswith(self._blog_config.temp_dir):
            markdown = re.sub(MARKDOWN_FILE_RE, self._fix_blog_main_paths, markdown)
        return markdown
