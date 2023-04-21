import logging
import re
from dataclasses import dataclass
from typing import Dict
from typing import List
from typing import Optional
from typing import cast

from mkdocs.config.defaults import MkDocsConfig
from mkdocs.structure.pages import Page
from pymdownx.slugs import slugify

from mkdocs_publisher.blog.plugin import BlogPlugin

log = logging.getLogger("mkdocs.plugins.publisher.obsidian.backlinks")

MARKDOWN_LINK = re.compile(r"\[([^][\r\n]+)]\(((?!https?://)[^][)(\s]+.md)(#[\w\-.]+)?\)")
HTTP_LINK = re.compile(r"\[([^][\r\n]+)]\((https?://[^][)(\s]+)(#[\w\-.]+)?\)")


@dataclass()
class Link:
    text: str
    destination: str
    title: str
    source: str


class Backlink:
    def __init__(
        self,
        mkdocs_config: MkDocsConfig,
        links: Dict[str, List[Link]],
    ):
        self._mkdocs_config: MkDocsConfig = mkdocs_config
        self._links: Dict[str, List[Link]] = links

    @staticmethod
    def _build_anchor_link(backlink: str, anchor_link: Optional[str]) -> str:
        """Create backlink anchor link"""

        anchor_link = f"{backlink}{anchor_link}"
        for r in (("../", ""), (".md", ""), ("#", " "), ("/", " "), ("_", "-")):
            anchor_link = anchor_link.replace(*r)
        return slugify(case="lower")(text=anchor_link, sep="-")

    @staticmethod
    def _replace_fake_link(match: re.Match) -> str:
        """Return only a text from a link (http or markdown file)"""

        return match.group(1)

    def _create_anchor_link(self, match: re.Match):
        """Create an a backlink with an additional anchor link"""
        anchor_link = match.group(3) if match.group(3) is not None else ""
        backlink = match.group(2)
        backlink_anchor_link = self._build_anchor_link(backlink=backlink, anchor_link=anchor_link)
        return f"[{match.group(1)}]({backlink}{anchor_link}){{ #{backlink_anchor_link} }}"

    def _parse_markdown_link(self, match: re.Match, page: Page, line: str):
        anchor_link = match.group(3) if match.group(3) is not None else ""
        original_link_destination = match.group(2)
        original_link_text = f"[{match.group(1)}]({original_link_destination}{anchor_link})"
        anchor_link = self._build_anchor_link(
            backlink=original_link_destination, anchor_link=anchor_link
        )
        backlink_link = f"{self._mkdocs_config.site_url}{page.url}#{anchor_link}"

        # Convert document link into backlink
        link_replacement = f'<a href="{backlink_link}">{match.group(1)}</a>'
        backlink_text = line.replace(original_link_text, link_replacement)

        # Convert other links into text
        backlink_text = re.sub(MARKDOWN_LINK, self._replace_fake_link, backlink_text)
        backlink_text = re.sub(HTTP_LINK, self._replace_fake_link, backlink_text)

        # Create a backlink with context
        backlink_text = f'<p class="obsidian_backlink">{backlink_text}</p>'

        # Convert relative links into absolute links inside document directory
        original_link_source = page.file.src_uri
        if len(original_link_destination.split("/")) == 1:
            destination_pre = original_link_source.split("/")[:-1]
            destination_pre.append(original_link_destination)
            original_link_destination = "/".join(destination_pre)
        original_link_destination = original_link_destination.replace("../", "")

        link = Link(
            text=backlink_text,
            destination=backlink_link,
            source=original_link_destination,
            title=str(page.title),
        )

        # Get blog temporary files
        temp_blog_files = []
        if "pub-blog" in self._mkdocs_config.plugins:
            blog_plugin: BlogPlugin = cast(BlogPlugin, self._mkdocs_config.plugins["pub-blog"])
            temp_blog_files = blog_plugin.blog_config.temp_files_list

        # Do not add backlink if links points to the same document
        if (
            original_link_source != original_link_destination
            and original_link_source not in temp_blog_files
        ):
            if original_link_destination not in self._links:
                self._links[original_link_destination] = [link]
            else:
                link_found = False
                for existing_link in self._links[original_link_destination]:
                    # Add backlink to an existing one
                    if existing_link.title == link.title:
                        link_found = True
                        existing_link.text = f"{existing_link.text}<hr>{link.text}"
                if not link_found:
                    self._links[original_link_destination].append(link)

    def find_markdown_links(self, markdown: str, page: Page):
        """Find all markdown links"""
        for line in markdown.split("\n"):
            for match in re.finditer(MARKDOWN_LINK, line):
                self._parse_markdown_link(match=match, page=page, line=line)

    def convert_to_anchor_link(self, markdown: str) -> str:
        """Convert backlink to link with an anchor for direct navigation after clicking on it"""
        return re.sub(MARKDOWN_LINK, self._create_anchor_link, markdown)
