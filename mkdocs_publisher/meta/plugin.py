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

import contextlib
import logging
from datetime import datetime
from pathlib import Path
from typing import Literal

from mkdocs.config import Config
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.plugins import BasePlugin
from mkdocs.plugins import event_priority
from mkdocs.structure.files import Files
from mkdocs.structure.nav import Navigation
from mkdocs.structure.pages import Page

from mkdocs_publisher._shared import publisher_utils
from mkdocs_publisher.meta.config import MetaPluginConfig
from mkdocs_publisher.meta.meta_files import MetaFiles
from mkdocs_publisher.meta.meta_nav import MetaNav

log = logging.getLogger("mkdocs.publisher.meta.plugin")


class MetaPlugin(BasePlugin[MetaPluginConfig]):
    supports_multiple_instances = False

    def __init__(self):
        self._on_serve: bool = False
        self._attachments_dir: Path | None = None
        self._ignored_dirs: list[Path] = []
        self._meta_files: MetaFiles = MetaFiles()
        self._meta_nav: MetaNav | None = None

    def on_startup(self, *, command: Literal["build", "gh-deploy", "serve"], dirty: bool) -> None:  # pragma: no cover
        if command == "serve":
            self._on_serve = True
        self._meta_files.on_serve = self._on_serve

    @event_priority(100)  # Run before any other plugins
    def on_config(self, config: MkDocsConfig) -> Config | None:  # pragma: no cover
        # Set some default values
        log.info("Read files and directories metadata")
        blog_dir: Path | None = publisher_utils.get_blog_dir(mkdocs_config=config)
        self._meta_nav = MetaNav(
            meta_files=self._meta_files,
            blog_dir=blog_dir.relative_to(config.docs_dir) if blog_dir else blog_dir,
        )
        self._ignored_dirs, self._attachments_dir = publisher_utils.get_obsidian_dirs(mkdocs_config=config)
        self._meta_files.set_configs(mkdocs_config=config, meta_plugin_config=self.config)
        self._meta_files.add_hidden_path(hidden_path=self._attachments_dir)
        self._meta_files.add_files(ignored_dirs=self._ignored_dirs)

        log.info(f"Ignored directories: " f"{[str(d.relative_to(config.docs_dir)) for d in self._ignored_dirs]}")
        log.info(f"Draft files and directories: " f"{list(self._meta_files.drafts.keys())}")
        log.info(f"Hidden files and directories: " f"{list(self._meta_files.hidden.keys())}")

        config.nav = self._meta_nav.build_nav(mkdocs_config=config)

        return config

    @event_priority(-100)
    def on_files(self, files: Files, *, config: MkDocsConfig) -> Files | None:  # pragma: no cover
        new_files = self._meta_files.clean_redirect_files(files=files)
        new_files = self._meta_files.change_files_slug(files=new_files, ignored_dirs=self._ignored_dirs)
        new_files = self._meta_files.clean_draft_files(files=new_files)

        return new_files

    def on_nav(self, nav: Navigation, *, config: MkDocsConfig, files: Files) -> Navigation | None:  # pragma: no cover
        removal_list = [*self._meta_files.drafts.keys(), *self._meta_files.hidden.keys()]
        log.debug(f"Nav elements to remove: {removal_list}")
        nav.items = self._meta_nav.nav_cleanup(
            items=nav.items,
            removal_list=removal_list,
        )

        # TODO: create prev/next page cleanup for hidden pages

        return nav

    @event_priority(-100)  # Run after all other plugins
    def on_page_markdown(self, markdown: str, *, page: Page, config: MkDocsConfig, files: Files):
        # Modify page update date
        # TODO: move date format to config
        # TODO: warn on missing in config
        update_date: datetime = page.meta.get(
            "update", page.meta.get("date", datetime.strptime(page.update_date, "%Y-%m-%d"))
        )
        with contextlib.suppress(AttributeError):
            page.update_date = update_date.strftime("%Y-%m-%d")

        # Conditionally exclude file from Material for MkDocs search plugin
        if (  # pragma: no cover
            page.file.src_uri in self._meta_files.draft_files and not self.config.publish.search_in_draft
        ) or (page.file.src_uri in self._meta_files.hidden_files and not self.config.publish.search_in_hidden):
            page.meta["search"] = {"exclude": True}

    @event_priority(-100)  # Run after all other plugins
    def on_post_page(self, output: str, *, page: Page, config: MkDocsConfig) -> str | None:  # pragma: no cover
        if page.file.src_path in self._meta_files:
            redirect_page: str | None = self._meta_files.generate_redirect_page(file=page.file)
            if redirect_page:
                output = redirect_page
        return output

    # TODO: sitemap modification for hidden, draft and by frontmatter
    # def on_post_template(self, output_content: str, /, *, template_name: str, config: MkDocsConfig) -> Optional[str]:
    #     if template_name == "sitemap.xml":
    #         log.warning(template_name)
    #         log.warning(output_content)
