import logging
import re
from pathlib import Path
from typing import Optional

from mkdocs.config.defaults import MkDocsConfig
from mkdocs.plugins import BasePlugin
from mkdocs.structure.files import Files
from mkdocs.structure.pages import Page

from mkdocs_publisher.obsidian.config import ObsidianPluginConfig

log = logging.getLogger("mkdocs.plugins.publisher.obsidian")

MARKDOWN_LINKS = r"\[(\S+)]\(((?!http.?://)\S+.md)\)"


class ObsidianPlugin(BasePlugin[ObsidianPluginConfig]):
    def on_page_markdown(
        self, markdown: str, *, page: Page, config: MkDocsConfig, files: Files
    ) -> Optional[str]:
        def _link_normalization_callback(match: re.Match):
            link_name, link_file_path = match.groups()
            link_parts = list(Path(link_file_path).parts)
            while True:
                if link_parts[0] == Path(config.docs_dir).parts[-1]:
                    link_parts.pop(0)
                else:
                    break
            link_file_path = Path(*link_parts)
            return f"[{link_name}]({link_file_path})"

        if page.title == "test":
            markdown = re.sub(MARKDOWN_LINKS, _link_normalization_callback, markdown)

        return markdown
