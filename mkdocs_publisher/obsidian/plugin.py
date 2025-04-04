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
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence  # noqa: UP035

import watchdog.events
from mkdocs.config import Config
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.livereload import LiveReloadServer
from mkdocs.plugins import BasePlugin
from mkdocs.plugins import event_priority
from mkdocs.structure.files import Files
from mkdocs.structure.nav import Navigation
from mkdocs.structure.pages import Page

from mkdocs_publisher._shared import mkdocs_utils
from mkdocs_publisher._shared import publisher_utils
from mkdocs_publisher._shared import resources
from mkdocs_publisher._shared import templates
from mkdocs_publisher._shared.html_modifiers import HTMLModifier
from mkdocs_publisher.obsidian.backlinks import BacklinkLinks
from mkdocs_publisher.obsidian.backlinks import Link
from mkdocs_publisher.obsidian.callouts import CalloutToAdmonition
from mkdocs_publisher.obsidian.config import ObsidianPluginConfig
from mkdocs_publisher.obsidian.md_links import MarkdownLinks
from mkdocs_publisher.obsidian.vega import VegaCharts

COMMENTS_RE = re.compile(r"%%(?P<comment>[^%%]+)%%")

log = logging.getLogger("mkdocs.publisher.obsidian.plugin")


@dataclass
class Comment:
    comment: str
    is_html_comment: bool | None = False

    def __repr__(self) -> str:
        return f"<!--{self.comment}-->" if self.is_html_comment else ""


class ObsidianPlugin(BasePlugin[ObsidianPluginConfig]):
    supports_multiple_instances = False

    def __init__(self) -> None:
        self._backlink_links: BacklinkLinks | None = None
        self._backlinks: dict[str, list[Link]] = {}
        self._ignored_dirs: list[Path] = []
        self._md_links: MarkdownLinks | None = None
        self._vega_pages: list[Page] = []

    def _normalize_comments(self, match: re.Match) -> str:
        comment = Comment(**match.groupdict())
        comment.is_html_comment = self.config.comments.inject_as_html
        return str(comment)

    def on_config(self, config: MkDocsConfig) -> Config | None:
        self._backlink_links = BacklinkLinks(mkdocs_config=config, backlinks=self._backlinks)
        self._md_links = MarkdownLinks(mkdocs_config=config)
        self._ignored_dirs, _ = publisher_utils.get_obsidian_dirs(mkdocs_config=config)
        ignored_dirs: str = ", ".join([f"'{d.relative_to(config.docs_dir)}'" for d in self._ignored_dirs])
        log.info(f"Obsidian ignored directories: {ignored_dirs}")
        return config

    def files_cleanup(self, files: Files, removal_list: Sequence[str | Path]) -> Files:
        removal_list = [str(p) for p in removal_list]
        new_files = Files(files=[])
        for file in files:
            if str(Path(file.src_path).parent) not in removal_list:
                new_files.append(file=file)

        return new_files

    def on_files(self, files: Files, *, config: MkDocsConfig) -> Files | None:
        files = self.files_cleanup(files=files, removal_list=self._ignored_dirs)

        if self.config.vega.enabled:
            resources.add_extra_css(
                stylesheet_file_name="obsidian.min.css",
                config=config,
                files=files,
            )
        return files

    def on_nav(self, nav: Navigation, *, config: MkDocsConfig, files: Files) -> Navigation | None:  # noqa: ARG002
        nav.items = publisher_utils.nav_cleanup(items=nav.items, removal_list=self._ignored_dirs)

        if self.config.backlinks.enabled:
            log.info("Parsing backlinks")
            for file in files:
                if file.page is not None:
                    log.debug(f"Parsing backlinks in file '{file.src_path}'")
                    markdown, _ = mkdocs_utils.read_md_file(md_file_path=Path(str(file.abs_src_path)))
                    markdown = self._md_links.normalize_links(markdown=markdown, current_file_path=Path(file.src_uri))
                    self._backlink_links.find_markdown_links(markdown=markdown, page=file.page)
        return nav

    @event_priority(100)  # Run before all other plugins
    def on_page_markdown(self, markdown: str, *, page: Page, config: MkDocsConfig, files: Files) -> str | None:  # noqa: ARG002
        # TODO: add verification if relative backlinks are enabled in .obsidian config
        markdown = self._md_links.normalize_links(markdown=markdown, current_file_path=Path(page.file.src_uri))
        if self.config.comments.enabled:
            markdown = re.sub(COMMENTS_RE, self._normalize_comments, markdown)

        if self.config.callouts.enabled:
            # TODO: add verification if all things are enabled in mkdocs.yaml config file
            callout_to_admonition = CalloutToAdmonition(callouts_config=self.config.callouts)
            markdown = callout_to_admonition.convert_callouts(markdown=markdown, file_path=str(page.file.src_uri))

        if self.config.vega.enabled:
            # TODO: add verification if all things are enabled in .obsidian config
            vega_charts = VegaCharts(vega_config=self.config.vega)
            markdown = vega_charts.generate_charts(markdown=markdown)
            if vega_charts.is_vega:
                self._vega_pages.append(page)

        if self.config.backlinks.enabled:
            markdown = self._backlink_links.convert_to_backlink(markdown=markdown)
            page_backlinks = self._backlinks.get(f"{page.file.src_uri}", None)
            if page_backlinks is not None:
                log.debug(f"Adding backlinks to '{page.file.src_uri}'")
                backlink_context = {
                    "backlinks": page_backlinks,
                    "title": "Backlinks",  # TODO: move to translations
                }
                backlink_render = templates.render(tpl_file="backlinks.html", context=backlink_context)
                markdown = f"{markdown}{backlink_render}"
        return markdown

    def on_post_page(self, output: str, *, page: Page, config: MkDocsConfig) -> str | None:  # noqa: ARG002
        if self.config.vega.enabled and page in self._vega_pages:
            # TODO: embed scripts to assets and give possibility to serve from site_dir
            # TODO: add a tool to check if those libraries are the in the latest version
            html_modifier = HTMLModifier(markup=output)
            html_modifier.add_head_script(src="https://cdn.jsdelivr.net/npm/vega@5.22.1")
            html_modifier.add_head_script(src="https://cdn.jsdelivr.net/npm/vega-lite@5.6.1")
            html_modifier.add_head_script(src="https://cdn.jsdelivr.net/npm/vega-embed@6.21.2")
            output = str(html_modifier)

        return output

    # ruff: noqa: SLF001
    def on_serve(self, server: LiveReloadServer, *, config: MkDocsConfig, builder: Callable) -> LiveReloadServer | None:  # noqa: ARG002
        server.unwatch(config.docs_dir)

        docs_dirs_to_skip = [str(Path(config.docs_dir) / self.config.obsidian_dir)]

        def no_obsidian_callback(event) -> None:  # noqa: ANN001
            """Watcher implementation that skips .obsidian directory"""
            if (
                isinstance(event, watchdog.events.FileModifiedEvent)
                and any(str(event.src_path).startswith(d) for d in docs_dirs_to_skip)
                or event.is_directory
            ):
                return

            with server._rebuild_cond:
                server._want_rebuild = True
                server._rebuild_cond.notify_all()

        handler = watchdog.events.FileSystemEventHandler()
        handler.on_any_event = no_obsidian_callback

        if config.docs_dir in server._watched_paths:
            server._watched_paths[config.docs_dir] += 1
            return None
        server._watched_paths[config.docs_dir] = 1

        server._watch_refs[config.docs_dir] = server.observer.schedule(handler, config.docs_dir, recursive=True)
        log.debug(f"Watching '{config.docs_dir}'")
        return server
