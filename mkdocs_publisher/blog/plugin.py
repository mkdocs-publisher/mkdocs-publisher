import logging
from collections import OrderedDict
from pathlib import Path
from typing import Any
from typing import Dict
from typing import Literal
from typing import Optional
from typing import cast

from mkdocs.config import Config
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.plugins import BasePlugin
from mkdocs.plugins import event_priority
from mkdocs.structure.files import Files
from mkdocs.structure.nav import Navigation
from mkdocs.structure.pages import Page

# noinspection PyProtectedMember
from mkdocs_publisher._shared import file_utils
from mkdocs_publisher._shared import resources
from mkdocs_publisher.blog import creators
from mkdocs_publisher.blog import modifiers
from mkdocs_publisher.blog import parsers
from mkdocs_publisher.blog.config import BlogPluginConfig
from mkdocs_publisher.blog.structures import BlogConfig

log = logging.getLogger("mkdocs.plugins.publisher.blog.plugin")


class BlogPlugin(BasePlugin[BlogPluginConfig]):
    def __init__(self):
        self.blog_config = BlogConfig()  # Empty instance
        self._start_page: bool = False
        self._on_serve: bool = False

    def on_startup(self, *, command: Literal["build", "gh-deploy", "serve"], dirty: bool) -> None:
        if command == "serve":
            self._on_serve = True

    def on_config(self, config: MkDocsConfig) -> Config:

        # Initialization of all the values
        self.blog_config.parse_configs(mkdocs_config=config, plugin_config=self.config)

        # Modify nav section
        if config.nav is None:
            config.nav = [{str(self.blog_config.blog_dir): str(self.blog_config.blog_dir)}]

        # Detect if blog is a starting page
        if len(config.nav) > 0:
            first_value = list(config.nav[0].values())[0]
            if isinstance(first_value, str) and first_value == str(self.blog_config.blog_dir):
                self._start_page = True

        # New config navigation
        config_nav = OrderedDict()
        parsers.parse_markdown_files(
            blog_config=self.blog_config,
            config_nav=config_nav,
            on_serve=self._on_serve,
        )

        parsers.create_blog_post_teaser(
            blog_config=self.blog_config,
        )

        creators.create_blog_post_pages(
            start_page=self._start_page,
            blog_config=self.blog_config,
            config_nav=config_nav,
        )

        modifiers.blog_post_nav_sorter(
            blog_config=self.blog_config,
            config_nav=config_nav,
        )

        # Inject blog into navigation
        new_nav = []
        for nav_item in cast(list, config.nav):
            if str(self.blog_config.blog_dir) in nav_item.values():
                for k, v in config_nav.items():
                    new_nav.append({k: v})
            else:
                new_nav.append(nav_item)
        config.nav = new_nav

        return config

    def on_nav(self, nav: Navigation, config: MkDocsConfig, files: Files) -> Navigation:

        modifiers.blog_post_nav_remove(
            start_page=self._start_page, blog_config=self.blog_config, nav=nav
        )

        return nav

    def on_files(self, files: Files, config: MkDocsConfig) -> Files:

        creators.create_blog_files(blog_config=self.blog_config, files=files)

        resources.add_extra_css(stylesheet_file_name="blog.min.css", config=config, files=files)

        return files

    @event_priority(-100)  # Run after all other plugins
    def on_page_context(
        self, context: Dict[str, Any], *, page: Page, config: MkDocsConfig, nav: Navigation
    ) -> Optional[Dict[str, Any]]:

        if Path(page.file.src_path).parts[0] == self.config.blog_dir:
            page.meta[self.config.comments.key_name] = self.config.comments.enabled

        # Temporary created files cannot be edited
        if page.file.src_uri in self.blog_config.temp_files_list:
            page.edit_url = None

        modifiers.blog_post_nav_next_prev_change(
            start_page=self._start_page, blog_config=self.blog_config, page=page
        )
        return context

    @event_priority(-100)  # Run after all other plugins
    def on_build_error(self, error: Exception) -> None:

        file_utils.remove_dir(directory=self.blog_config.temp_dir)

    @event_priority(-100)  # Run after all other plugins
    def on_shutdown(self) -> None:

        file_utils.remove_dir(directory=self.blog_config.temp_dir)
