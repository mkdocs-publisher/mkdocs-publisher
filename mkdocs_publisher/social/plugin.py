import logging
from pathlib import Path
from typing import List
from typing import Optional

from bs4 import BeautifulSoup
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.plugins import BasePlugin
from mkdocs.plugins import event_priority
from mkdocs.structure.pages import Page

from mkdocs_publisher.social.config import SocialConfig

log = logging.getLogger("mkdocs.plugins.publisher.social")

TWITTER_PROPERTIES = [
    "twitter:title",
    "twitter:description",
    "twitter:image",
    "twitter:card",
    "twitter:site",
    "twitter:creator",
]
OPEN_GRAPH_PROPERTIES = [
    "og:title",
    "og:description",
    "og:type",
    "og:url",
    "og:image",
    "og:site_name",
    "og:locale",
]


def _remove_properties_from_head(soup: BeautifulSoup, properties: List[str]):
    """Remove meta tags with given properties from HTML head section"""
    for prop in properties:
        head_property = soup.head.find(name="meta", attr={"property": prop})  # type: ignore
        if head_property is not None:
            head_property.extract()


def _add_meta_property(soup: BeautifulSoup, name: str, value: str):
    soup.head.append(soup.new_tag(name="meta", attrs={"property": name, "content": value}))  # type: ignore


class SocialPlugin(BasePlugin[SocialConfig]):
    @event_priority(-99)
    def on_post_page(self, output: str, *, page: Page, config: MkDocsConfig) -> Optional[str]:
        soup: BeautifulSoup = BeautifulSoup(markup=output, features="html.parser")

        # Remove old values
        _remove_properties_from_head(soup=soup, properties=OPEN_GRAPH_PROPERTIES)
        _remove_properties_from_head(soup=soup, properties=TWITTER_PROPERTIES)

        # Get all needed meta values
        title = page.meta.get(self.config.meta_keys.title_key, None)
        description = page.meta.get(self.config.meta_keys.description_key, None)
        image = page.meta.get(self.config.meta_keys.image_key, None)
        if image is not None:
            image_path = Path(config.docs_dir) / Path(
                image[1:] if str(image).startswith("/") else image
            )
            if not image_path.exists():
                log.warning(
                    f"File: '{str(image)}' doesn't exists!\n"
                    f"('{self.config.meta_keys.image_key}' meta key"
                    f" from '{page.file.src_path}' file.)"
                )
            image = f"{config.site_url}{image}".replace("//", "/")
        url = f"{config.site_url}{page.url}"
        site_name = config.site_name
        # Add all open graph values
        if self.config.og.enabled and title and description:
            _add_meta_property(soup=soup, name="og:type", value="article")
            _add_meta_property(soup=soup, name="og:title", value=title)
            _add_meta_property(soup=soup, name="og:description", value=description)
            _add_meta_property(soup=soup, name="og:site_name", value=site_name)
            _add_meta_property(soup=soup, name="og:locale", value=self.config.og.locale)
            _add_meta_property(soup=soup, name="og:url", value=url)

            if image is not None:
                _add_meta_property(soup=soup, name="og:image", value=image)

        # Add all twitter values
        if self.config.twitter.enabled and title and description:
            card_type = "summary_large_image" if image else "summary"
            _add_meta_property(soup=soup, name="twitter:card", value=card_type)
            _add_meta_property(soup=soup, name="twitter:title", value=title)
            _add_meta_property(soup=soup, name="twitter:description", value=description)

            if image is not None:
                _add_meta_property(soup=soup, name="twitter:image", value=image)

            if self.config.twitter.website:
                _add_meta_property(
                    soup=soup, name="twitter:site", value=self.config.twitter.website
                )

            if self.config.twitter.author:
                _add_meta_property(
                    soup=soup, name="twitter:creator", value=self.config.twitter.author
                )

        return soup.prettify()
