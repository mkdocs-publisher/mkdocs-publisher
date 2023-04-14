import importlib
import importlib.resources
import importlib.util
import logging
import re
from typing import Callable
from typing import Optional

from bs4 import BeautifulSoup
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.livereload import LiveReloadServer
from mkdocs.plugins import BasePlugin
from mkdocs.structure.files import File
from mkdocs.structure.files import Files
from mkdocs.structure.pages import Page

from mkdocs_publisher.obsidian.callout import CalloutToAdmonition
from mkdocs_publisher.obsidian.config import ObsidianPluginConfig
from mkdocs_publisher.obsidian.vega import VegaCharts

log = logging.getLogger("mkdocs.plugins.publisher.obsidian")

WIKI_LINKS = r"(\[\[\S+\]\])"


def _wiki_link_normalization_callback(match: re.Match):
    wiki_link = match.group(0)[2:-2]
    # TODO: not only .md files can be inside wiki linki (also images). Fix extensions
    if "|" in wiki_link:
        file, name = wiki_link.split("|")
        wiki_link = f"[{name}]({file}.md)"
    else:
        name = wiki_link.split("/")[-1]
        wiki_link = f"[{name}]({wiki_link}.md)"
    return wiki_link


class ObsidianPlugin(BasePlugin[ObsidianPluginConfig]):
    def on_page_markdown(
        self, markdown: str, *, page: Page, config: MkDocsConfig, files: Files
    ) -> Optional[str]:

        if self.config.wiki_links_enabled:
            markdown = re.sub(WIKI_LINKS, _wiki_link_normalization_callback, markdown)

        if self.config.callouts.enabled:
            # TODO: add verification if all things are enabled in mkdocs.yaml config file
            callout_to_admonition = CalloutToAdmonition(callouts_config=self.config.callouts)
            markdown = callout_to_admonition.convert_callouts(markdown=markdown)

        if self.config.vega.enabled:
            vega_charts = VegaCharts(vega_config=self.config.vega)
            markdown = vega_charts.generate_charts(markdown=markdown)

        return markdown

    def on_files(self, files: Files, *, config: MkDocsConfig) -> Optional[Files]:
        if self.config.vega.enabled:
            config.extra_css.append("assets/stylesheets/obsidian.css")

            with importlib.resources.path(
                importlib.import_module("mkdocs_publisher._extra"), "__init__.py"
            ) as extra_path:
                s = importlib.import_module("mkdocs_publisher._extra.assets.stylesheets")
                with importlib.resources.path(s, "obsidian.css") as blog_stylesheets:
                    files.append(
                        File(
                            path=str(blog_stylesheets.relative_to(extra_path.parent)),
                            src_dir=str(extra_path.parent),
                            dest_dir=config.site_dir,
                            use_directory_urls=config.use_directory_urls,
                        )
                    )

        return files

    def on_post_page(self, output: str, *, page: Page, config: MkDocsConfig) -> Optional[str]:
        soup: BeautifulSoup = BeautifulSoup(markup=output, features="html.parser")

        if self.config.vega.enabled:
            soup.head.append(  # type: ignore
                soup.new_tag(
                    name="script", attrs={"src": "https://cdn.jsdelivr.net/npm/vega@5.22.1"}
                )
            )
            soup.head.append(  # type: ignore
                soup.new_tag(
                    name="script", attrs={"src": "https://cdn.jsdelivr.net/npm/vega-lite@5.6.1"}
                )
            )
            soup.head.append(  # type: ignore
                soup.new_tag(
                    name="script", attrs={"src": "https://cdn.jsdelivr.net/npm/vega-embed@6.21.2"}
                )
            )

        return soup.prettify()

    def on_serve(
        self, server: LiveReloadServer, *, config: MkDocsConfig, builder: Callable
    ) -> Optional[LiveReloadServer]:
        server.unwatch(config.docs_dir)

        return server
