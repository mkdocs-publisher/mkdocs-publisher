import importlib
import importlib.resources
import importlib.util
import logging
from pathlib import Path
from typing import Callable
from typing import Dict
from typing import List
from typing import Optional
from typing import cast

import jinja2
import watchdog.events
from mkdocs.config import Config
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.livereload import LiveReloadServer
from mkdocs.plugins import BasePlugin
from mkdocs.plugins import event_priority
from mkdocs.structure.files import Files
from mkdocs.structure.nav import Navigation
from mkdocs.structure.pages import Page
from mkdocs.utils import meta as meta_parser

from mkdocs_publisher._common import resources
from mkdocs_publisher._common.html_modifiers import HTMLModifier
from mkdocs_publisher._extra.assets import templates
from mkdocs_publisher.obsidian.backlinks import Backlink
from mkdocs_publisher.obsidian.backlinks import Link
from mkdocs_publisher.obsidian.callout import CalloutToAdmonition
from mkdocs_publisher.obsidian.config import ObsidianPluginConfig
from mkdocs_publisher.obsidian.md_links import MarkdownLinks
from mkdocs_publisher.obsidian.vega import VegaCharts

log = logging.getLogger("mkdocs.plugins.publisher.obsidian")


class ObsidianPlugin(BasePlugin[ObsidianPluginConfig]):
    def __init__(self):
        self._backlink: Backlink = cast(Backlink, None)
        self._backlink_links: Dict[str, List[Link]] = {}
        self._md_links: MarkdownLinks = cast(MarkdownLinks, None)
        self._vega_pages: List[Page] = list()

    def on_config(self, config: MkDocsConfig) -> Optional[Config]:
        self._backlink = Backlink(mkdocs_config=config, backlinks=self._backlink_links)
        self._md_links = MarkdownLinks(mkdocs_config=config)
        return config

    def on_nav(
        self, nav: Navigation, *, config: MkDocsConfig, files: Files
    ) -> Optional[Navigation]:

        for file in files:
            if file.page is not None and self.config.backlinks.enabled:
                log.debug(f"Parse backlinks for backlinks in '{file.src_path}'")
                with open(file.abs_src_path, encoding="utf-8-sig", errors="strict") as md_file:
                    markdown, meta = meta_parser.get_data(md_file.read())

                    markdown = self._md_links.normalize(
                        markdown=markdown, file_path=str(file.src_uri)
                    )

                    self._backlink.find_markdown_links(markdown=markdown, page=file.page)
        return nav

    @event_priority(100)  # Run before all other plugins
    def on_page_markdown(
        self, markdown: str, *, page: Page, config: MkDocsConfig, files: Files
    ) -> Optional[str]:
        # TODO: add verification if relative backlinks are enabled in .obsidian config
        markdown = self._md_links.normalize(markdown=markdown, file_path=str(page.file.src_uri))

        if self.config.callouts.enabled:
            # TODO: add verification if all things are enabled in mkdocs.yaml config file
            callout_to_admonition = CalloutToAdmonition(callouts_config=self.config.callouts)
            markdown = callout_to_admonition.convert_callouts(
                markdown=markdown, file_path=str(page.file.src_uri)
            )

        if self.config.vega.enabled:
            # TODO: add verification if all things are enabled in .obsidian config
            vega_charts = VegaCharts(vega_config=self.config.vega)
            markdown = vega_charts.generate_charts(markdown=markdown)
            if vega_charts.is_vega:
                self._vega_pages.append(page)

        if self.config.backlinks.enabled:
            markdown = self._backlink.convert_to_anchor_link(markdown=markdown)
            page_backlinks = self._backlink_links.get(f"{page.file.src_uri}", None)
            if page_backlinks is not None:
                log.debug(f"Add backlinks to '{page.file.src_uri}'")
                backlink_template = importlib.resources.read_text(templates, "backlinks.html")
                context = {
                    "backlinks": page_backlinks,
                    "title": "Backlinks",  # TODO: move to translations
                }
                template = jinja2.Environment(loader=jinja2.BaseLoader()).from_string(
                    backlink_template
                )
                markdown = f"{markdown}{template.render(context)}"
        return markdown

    def on_files(self, files: Files, *, config: MkDocsConfig) -> Optional[Files]:
        if self.config.vega.enabled:
            resources.add_extra_css(
                stylesheet_file_name="obsidian.min.css",
                config=config,
                files=files,
            )
        return files

    def on_post_page(self, output: str, *, page: Page, config: MkDocsConfig) -> Optional[str]:

        if self.config.vega.enabled and page in self._vega_pages:
            # TODO: embed scripts to assets and give possibility to serve from site_dir
            html_modifier = HTMLModifier(markup=output)
            html_modifier.add_head_script(src="https://cdn.jsdelivr.net/npm/vega@5.22.1")
            html_modifier.add_head_script(src="https://cdn.jsdelivr.net/npm/vega-lite@5.6.1")
            html_modifier.add_head_script(src="https://cdn.jsdelivr.net/npm/vega-embed@6.21.2")
            output = str(html_modifier)

        return output

    def on_serve(
        self, server: LiveReloadServer, *, config: MkDocsConfig, builder: Callable
    ) -> Optional[LiveReloadServer]:
        server.unwatch(config.docs_dir)

        def no_obsidian_callback(event):
            """Watcheer implementation that skips .obsidian directory"""
            if isinstance(event, watchdog.events.FileModifiedEvent) and str(
                event.src_path
            ).startswith(str(Path(config.docs_dir) / self.config.obsidian_dir)):
                return

            if event.is_directory:
                return
            log.debug(str(event))
            with server._rebuild_cond:
                server._to_rebuild[server.builder] = True
                server._rebuild_cond.notify_all()

        handler = watchdog.events.FileSystemEventHandler()
        handler.on_any_event = no_obsidian_callback
        server._watch_refs[config.docs_dir] = server.observer.schedule(
            handler, config.docs_dir, recursive=True
        )

        return server
