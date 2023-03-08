import logging
from collections import OrderedDict
from datetime import datetime
from pathlib import Path
from typing import Any
from typing import Dict
from typing import Optional

from mkdocs.config import Config
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.plugins import BasePlugin
from mkdocs.plugins import event_priority
from mkdocs.structure.files import Files
from mkdocs.structure.nav import Navigation
from mkdocs.structure.pages import Page

import utils
from blog import creators
from blog import modifiers
from blog import parsers
from blog.config import BlogPluginConfig
from blog.structures import BlogConfig

log = logging.getLogger("mkdocs.plugins.publisher.blog")


class BlogPlugin(BasePlugin[BlogPluginConfig]):
    def __init__(self):
        self.blog_config = BlogConfig()  # Empty instance
        self.temp_files: Dict[str, Path] = {}

    def on_config(self, config: MkDocsConfig) -> Config:

        # Initialization of all the values
        self.blog_config.parse_configs(mkdocs_config=config, plugin_config=self.config)

        # New config navigation
        config_nav = OrderedDict()

        parsers.parse_markdown_files(
            blog_config=self.blog_config,
            config_nav=config_nav,
        )

        parsers.create_blog_post_teaser(
            blog_config=self.blog_config,
        )

        creators.create_blog_post_pages(
            blog_config=self.blog_config,
            config_nav=config_nav,
        )

        modifiers.blog_post_nav_sorter(
            blog_config=self.blog_config,
            config_nav=config_nav,
        )

        # Override nav section
        config.nav = config_nav
        return config

    def on_nav(self, nav: Navigation, config: MkDocsConfig, files: Files) -> Navigation:

        modifiers.blog_post_nav_remove(blog_config=self.blog_config, nav=nav)

        return nav

    def on_files(self, files: Files, config: MkDocsConfig) -> Files:

        creators.create_mkdocs_blog_files(blog_config=self.blog_config, files=files)

        new_files = modifiers.blog_post_slug_modifier(
            blog_config=self.blog_config,
            files=files,
        )

        return new_files

    @event_priority(-100)  # Run after all other plugins
    def on_page_markdown(self, markdown: str, *, page: Page, config: MkDocsConfig, files: Files):
        # Modify page update date
        # TODO: move date format to config
        update_date: datetime = page.meta.get(
            "update", page.meta.get("date", datetime.strptime(page.update_date, "%Y-%m-%d"))
        )
        page.update_date = update_date.strftime("%Y-%m-%d")

    @event_priority(-100)  # Run after all other plugins
    def on_page_context(
        self, context: Dict[str, Any], *, page: Page, config: MkDocsConfig, nav: Navigation
    ) -> Optional[Dict[str, Any]]:

        modifiers.blog_post_nav_next_prev_change(blog_config=self.blog_config, page=page)

        return context

    @event_priority(-100)  # Run after all other plugins
    def on_build_error(self, error: Exception) -> None:

        utils.remove_dir(directory=self.blog_config.temp_dir)

    @event_priority(-100)  # Run after all other plugins
    def on_shutdown(self) -> None:

        utils.remove_dir(directory=self.blog_config.temp_dir)
