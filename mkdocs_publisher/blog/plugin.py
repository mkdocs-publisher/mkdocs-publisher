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

import copy
import logging
import re
from pathlib import Path
from typing import Any
from typing import Literal
from typing import cast

from mkdocs.config import Config
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.plugins import BasePlugin
from mkdocs.plugins import event_priority
from mkdocs.structure.files import Files
from mkdocs.structure.nav import Navigation
from mkdocs.structure.pages import Page

from mkdocs_publisher._shared import links
from mkdocs_publisher._shared import mkdocs_utils
from mkdocs_publisher._shared import resources
from mkdocs_publisher.blog.blog_files import BlogFiles
from mkdocs_publisher.blog.config import BlogPluginConfig
from mkdocs_publisher.meta.config import MetaPluginConfig

"""
import contextlib
from collections import OrderedDict
from pathlib import Path

from mkdocs_publisher._shared import file_utils

from mkdocs_publisher.blog import creators
from mkdocs_publisher.blog import modifiers
from mkdocs_publisher.blog import parsers
from mkdocs_publisher.blog.structures import BlogConfig
from mkdocs_publisher.obsidian.md_links import MarkdownLinks
"""

log = logging.getLogger("mkdocs.publisher.blog.plugin")


class BlogPlugin(BasePlugin[BlogPluginConfig]):
    supports_multiple_instances = False  # TODO: add multiple instances support (require changes in meta plugin)

    def __init__(self) -> None:
        self._on_serve: bool = False
        self._start_page: bool = False
        self._blog_files: BlogFiles = BlogFiles()

    def on_startup(self, *, command: Literal["build", "gh-deploy", "serve"], dirty: bool) -> None:  # noqa: ARG002
        if command == "serve":
            self._on_serve = True
        self._blog_files.on_serve = self._on_serve

    def on_config(self, config: MkDocsConfig) -> Config:
        meta_plugin_config: MetaPluginConfig | None = mkdocs_utils.get_plugin_config(
            plugin_config_type=MetaPluginConfig,  # type: ignore[reportArgumentType]
            mkdocs_config=config,
        )
        self._blog_files.remove_old_temp_dirs(mkdocs_config=config)
        self._blog_files.set_configs(
            mkdocs_config=config,
            meta_plugin_config=meta_plugin_config,
            blog_plugin_config=self.config,
        )

        self._blog_files.add_blog_files()

        self._blog_files.generate_indexes()
        self._blog_files.generate_posts()
        # TODO: add tags and categories generation

        # TODO: move below code to blog_utils.py
        nav = []
        for nav_item in cast(list, config.nav):
            nav_item_value = next(iter(nav_item.values()))
            if isinstance(nav_item_value, list):
                nav_item_value_element = next(iter(nav_item_value[0].values()))
                if isinstance(nav_item_value_element, str) and Path(nav_item_value_element).is_relative_to(
                    Path(self.config.blog_dir),
                ):
                    nav.append({self.config.blog_dir: self._blog_files.nav})
                else:
                    nav.append(nav_item)
            else:
                nav.append(nav_item)

        # Detect if blog is a starting page
        if len(nav) > 0:
            first_value = next(iter(nav[0].keys()))
            if isinstance(first_value, str) and first_value == str(self.config.blog_dir):
                self._start_page = True

        config.nav = nav

        return config

    def on_nav(self, nav: Navigation, config: MkDocsConfig, files: Files) -> Navigation:  # noqa: ARG002
        """
        modifiers.blog_post_nav_remove(start_page=self._start_page, blog_config=self.blog_config, nav=nav)
        """

        # TODO: move below code to blog_utils.py
        for file in files:
            url_parts = file.dest_uri.replace(str(self._blog_files.blog_temp_path), self.config.blog_slug).split("/")
            if file.src_path.startswith(str(self._blog_files.blog_temp_path)):
                blog_file = self._blog_files.get_by_temp_file(temp_path=Path(file.src_path))
                if blog_file is not None:
                    for i, url_part in enumerate(url_parts):
                        if url_part == blog_file.path.stem:
                            url_parts[i] = str(blog_file.slug)

                file.dest_uri = "/".join(url_parts)
                file.url = "/".join(url_parts[0:-1])

                if file.url == self.config.blog_slug and self._start_page:
                    # log.warning(file)
                    file.dest_uri = file.dest_uri.split("/")[-1]
                    file.url = ""

        return nav

    def on_files(self, files: Files, config: MkDocsConfig) -> Files:
        resources.add_extra_css(stylesheet_file_name="blog.min.css", config=config, files=files)

        # TODO: move below code to blog_utils.py
        for file in copy.deepcopy(files):
            if Path(str(file.abs_src_path)).is_relative_to(str(self._blog_files.abs_blog_path)):
                files.remove(file=file)

        return files

    @event_priority(-100)  # Run after all other plugins
    def on_page_context(
        self,
        context: dict[str, Any],
        *,
        page: Page,
        config: MkDocsConfig,  # noqa: ARG002
        nav: Navigation,  # noqa: ARG002
    ) -> dict[str, Any] | None:
        """
        if Path(page.file.src_path).parts[0] == self.config.blog_dir:
            page.meta[self.config.comments.key_name] = self.config.comments.enabled

        # Temporary created files cannot be edited
        if page.file.src_uri in self.blog_config.temp_files_list:
            page.edit_url = None

        modifiers.blog_post_nav_next_prev_change(start_page=self._start_page, blog_config=self.blog_config, page=page)
        """
        return context

    @event_priority(-99)  # Run after all other plugins
    def on_page_markdown(self, markdown: str, *, page: Page, config: MkDocsConfig, files: Files) -> str | None:  # noqa: ARG002
        # TODO: move below code to blog_utils.py
        def _blog_relative_link_normalization(match: re.Match) -> str:
            """Normalize relative links to ensure they point to the correct location within the blog."""
            md_link_obj = links.LinkMatch(**match.groupdict())
            blog_posts_slug = self._blog_files._blog_plugin_config.posts.slug  # noqa: SLF001

            if md_link_obj.link.startswith("../") and Path(page.file.src_path).is_relative_to(
                str(self._blog_files.blog_temp_path.joinpath(blog_posts_slug)),
            ):
                md_link_obj.link = f"../{md_link_obj.link}"
            elif (
                not md_link_obj.link.startswith("../")
                and Path(page.file.src_path).parent == self._blog_files.blog_temp_path
            ):
                md_link_obj.link = f"{blog_posts_slug}/{md_link_obj.link}"
            elif Path(str(md_link_obj.link)).suffix != ".xml":
                link_elements = md_link_obj.link.split("/")
                if self.config.blog_dir in link_elements:
                    index = link_elements.index(self.config.blog_dir)
                    link = Path(link_elements[index]).joinpath(link_elements[index + 1])
                    if str(link) in self._blog_files:
                        link_elements[index] = str(self._blog_files.blog_temp_path.joinpath(blog_posts_slug))
                md_link_obj.link = str(Path(*link_elements))

            md_link = str(md_link_obj)
            log.debug(f"Replace md links pointing to blog files: {match.group(0)} > {md_link}")
            return md_link

        markdown = re.sub(links.RELATIVE_LINK_RE, _blog_relative_link_normalization, markdown)

        """
        # Dirty hack for blog standalone mode index file
        if page.file.src_path == "index.md":

            def _blog_index_re(match: re.Match):  # noqa: ANN202
                blog_link = links.LinkMatch(**match.groupdict())
                relative_path_finder = links.RelativePathFinder(
                    current_file_path=Path(page.file.src_path),
                    docs_dir=Path(config.docs_dir),
                    relative_path=Path(config.docs_dir),
                )
                full_blog_link = relative_path_finder.get_full_file_path(file_path=Path(str(blog_link.link)))
                blog_link.link = relative_path_finder.get_relative_file_path(file_path=full_blog_link)
                return str(blog_link)

            markdown = re.sub(links.RELATIVE_LINK_RE, _blog_index_re, markdown)
        """
        return markdown

    @event_priority(-100)  # Run after all other plugins
    def on_post_build(self, *, config: MkDocsConfig) -> None:  # noqa: ARG002
        self._blog_files.remove_temp_dirs()

        """
        # ==== Old below
        with contextlib.suppress(AttributeError):
            file_utils.remove_dir(directory=self.blog_config.temp_dir)
        """

    @event_priority(-100)  # Run after all other plugins
    def on_build_error(self, error: Exception) -> None:  # noqa: ARG002
        self._blog_files.remove_temp_dirs()

        """
        # ==== Old below
        with contextlib.suppress(AttributeError):
            file_utils.remove_dir(directory=self.blog_config.temp_dir)
        """

    @event_priority(-100)  # Run after all other plugins
    def on_shutdown(self) -> None:
        self._blog_files.remove_temp_dirs()

        """
        # ==== Old below
        with contextlib.suppress(AttributeError):
            file_utils.remove_dir(directory=self.blog_config.temp_dir)
        """
