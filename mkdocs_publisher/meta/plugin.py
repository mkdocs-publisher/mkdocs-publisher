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
from typing import Optional
from typing import cast
from urllib.parse import quote

from mkdocs.config import Config
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.plugins import BasePlugin
from mkdocs.plugins import event_priority
from mkdocs.structure.files import File
from mkdocs.structure.files import Files
from mkdocs.structure.nav import Navigation
from mkdocs.structure.pages import Page

from mkdocs_publisher._shared import mkdocs_utils

# noinspection PyProtectedMember
from mkdocs_publisher._shared.meta_files import MetaFile
from mkdocs_publisher._shared.meta_files import MetaFiles
from mkdocs_publisher.blog.config import BlogPluginConfig
from mkdocs_publisher.meta.config import MetaPluginConfig
from mkdocs_publisher.meta.nav import MetaNav
from mkdocs_publisher.obsidian.config import ObsidianPluginConfig

log = logging.getLogger("mkdocs.plugins.publisher.meta.plugin")


class MetaPlugin(BasePlugin[MetaPluginConfig]):
    def __init__(self):
        """
        TODO: SEO optimizations
        Useful links for sitemap.xml manipulation etc.:
        - https://octamedia.pl/blog/mapa-strony-xml/
        - https://octamedia.pl/blog/linkowanie-wewnetrzne/ (useful for obsidian backlinks)
        """

        self._on_serve = False  # TODO: change draft to published (pass it meta_files)
        self._blog_dir: Optional[Path] = None
        self._attachments_dir: Optional[Path] = None
        self._ignored_dirs: list[Path] = []
        self._meta_files: MetaFiles = MetaFiles()
        self._meta_nav: Optional[MetaNav] = None

    def on_startup(self, *, command: Literal["build", "gh-deploy", "serve"], dirty: bool) -> None:
        if command == "serve":
            self._on_serve = True
        self._meta_files.on_serve = self._on_serve

    @staticmethod
    def _get_blog_dir(mkdocs_config: MkDocsConfig) -> Optional[Path]:
        blog_config: Optional[BlogPluginConfig] = cast(
            BlogPluginConfig,
            mkdocs_utils.get_plugin_config(
                mkdocs_config=mkdocs_config,
                plugin_name="pub-blog",
            ),
        )
        if blog_config is not None:
            return Path(mkdocs_config.docs_dir).joinpath(blog_config.blog_dir)
        return None

    @staticmethod
    def _get_obsidian_dirs(mkdocs_config: MkDocsConfig) -> tuple[list[Path], Optional[Path]]:
        ignored_dirs: list[Path] = []
        attachments_dir: Optional[Path] = None
        docs_dir = Path(mkdocs_config.docs_dir)

        obsidian_config: Optional[ObsidianPluginConfig] = cast(
            ObsidianPluginConfig,
            mkdocs_utils.get_plugin_config(
                mkdocs_config=mkdocs_config,
                plugin_name="pub-obsidian",
            ),
        )
        if obsidian_config is not None:
            ignored_dirs.append(docs_dir.joinpath(obsidian_config.obsidian_dir))
            ignored_dirs.append(docs_dir.joinpath(obsidian_config.templates_dir))
            attachments_dir = docs_dir.joinpath(obsidian_config.attachments_dir)

        return ignored_dirs, attachments_dir

    @event_priority(100)  # Run before any other plugins
    def on_config(self, config: MkDocsConfig) -> Optional[Config]:
        # Set some default values
        log.info("Read files and directories metadata")
        self._blog_dir = self._get_blog_dir(mkdocs_config=config)
        self._meta_nav = MetaNav(
            meta_files=self._meta_files, blog_dir=self._blog_dir.relative_to(config.docs_dir)
        )
        self._ignored_dirs, self._attachments_dir = self._get_obsidian_dirs(mkdocs_config=config)
        self._meta_files.set_configs(mkdocs_config=config, meta_plugin_config=self.config)
        self._meta_files.add_hidden_path(hidden_path=self._attachments_dir)

        # Iterate over all files and directories in docs directory
        for docs_file in sorted(Path(config.docs_dir).rglob("*")):
            meta_link: Optional[MetaFile] = None
            is_ignored = any(
                [docs_file.is_relative_to(ignored_dir) for ignored_dir in self._ignored_dirs]
            )

            if not is_ignored and docs_file.is_dir():
                meta_link = MetaFile(
                    path=docs_file.relative_to(config.docs_dir),
                    abs_path=docs_file,
                    is_dir=True,
                )
            elif (
                not is_ignored
                and not docs_file.is_relative_to(cast(Path, self._blog_dir))
                and docs_file.suffix == ".md"
                and docs_file.name not in self._meta_files.meta_files
            ):
                meta_link = MetaFile(
                    path=docs_file.relative_to(config.docs_dir),
                    abs_path=docs_file,
                    is_dir=False,
                )

            if meta_link is not None:
                self._meta_files[str(meta_link.path)] = meta_link

        log.info(
            f"Ignored directories: "
            f"{[str(d.relative_to(config.docs_dir)) for d in self._ignored_dirs]}"
        )
        log.info(f"Draft files and directories: " f"{list(self._meta_files.drafts().keys())}")
        log.info(f"Hidden files and directories: " f"{list(self._meta_files.hidden().keys())}")

        config.nav = self._meta_nav.build_nav(mkdocs_config=config)

        return config

    @event_priority(-100)
    def on_files(self, files: Files, *, config: MkDocsConfig) -> Optional[Files]:
        draft_files = self._meta_files.drafts(files=True).keys()
        hidden_files = self._meta_files.hidden(files=True)

        ignored_dirs = [d.abs_path for d in self._meta_files.drafts(dirs=True).values()]
        ignored_dirs.extend(self._ignored_dirs)

        new_files = Files(files=[])
        for file in files:
            file: File
            file_path: Path = Path(file.src_path)

            if (
                not any([Path(file.abs_src_path).is_relative_to(d) for d in ignored_dirs])
                and file.src_path not in draft_files
                and file.src_path not in hidden_files
                and str(file_path.name) not in self._meta_files.meta_files
            ) or (
                str(file_path.name) in self._meta_files.meta_files
                and str(file_path.parent) in self._meta_files
                and self._meta_files[str(file_path.parent)].is_overview
            ):
                if self.config.slug.enabled:
                    # Get URL parts
                    if file.url.endswith("/"):
                        file.url = file.url[0:-1]
                    url_parts = file.url.split("/")

                    # Get abs file parts
                    path_parts: list[Path] = []
                    for path_part in file_path.parts:
                        if not path_parts:
                            path_parts.append(Path(path_part))
                        else:
                            path_parts.append(path_parts[-1] / path_part)

                    # Replace URL parts that have slug defined
                    for position, path_part in enumerate(path_parts):
                        meta_file: Optional[MetaFile] = self._meta_files.get(str(path_part), None)
                        if meta_file is not None:
                            url_parts[position] = meta_file.slug

                    # Recreate file params based on URL with replaced parts
                    if file.url != ".":  # Do not modify main index page
                        file.url = quote(f"{'/'.join(url_parts)}/")
                        url_parts.append(file.dest_uri.split("/")[-1])
                        if len(url_parts) >= 2 and url_parts[-1] == url_parts[-2]:
                            url_parts.pop(-1)
                        file.dest_uri = quote("/".join(url_parts))
                        file.abs_dest_path = str(Path(config.site_dir) / file.dest_uri)

                new_files.append(file)

        return new_files

    def on_nav(
        self, nav: Navigation, *, config: MkDocsConfig, files: Files
    ) -> Optional[Navigation]:
        removal_list = [*self._meta_files.drafts().keys(), *self._meta_files.hidden().keys()]

        log.info(f"Nav elements to remove: {removal_list}")

        nav.items = self._meta_nav.nav_cleanup(
            items=nav.items,
            removal_list=removal_list,
        )

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
        if (
            page.file.src_uri in self._meta_files.drafts(files=True)
            and not self.config.publish.search_in_draft
        ) or (
            page.file.src_uri in self._meta_files.hidden(files=True)
            and not self.config.publish.search_in_hidden
        ):
            page.meta["search"] = {"exclude": True}
