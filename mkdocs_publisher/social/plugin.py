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

import logging
from pathlib import Path
from typing import Optional

from mkdocs.config.defaults import MkDocsConfig
from mkdocs.plugins import BasePlugin
from mkdocs.plugins import event_priority
from mkdocs.structure.files import Files
from mkdocs.structure.pages import Page

from mkdocs_publisher._shared.html_modifiers import HTMLModifier
from mkdocs_publisher.social.config import SocialConfig
from mkdocs_publisher.social.config import TitleLocationChoiceEnum

log = logging.getLogger("mkdocs.publisher.social.plugin")

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


class SocialPlugin(BasePlugin[SocialConfig]):
    def on_page_markdown(self, markdown: str, *, page: Page, config: MkDocsConfig, files: Files) -> Optional[str]:
        pass

    @event_priority(-99)
    def on_post_page(self, output: str, *, page: Page, config: MkDocsConfig) -> Optional[str]:
        html_modifier = HTMLModifier(markup=output)

        log.debug(f"Processing social properties for file: '{page.file.src_path}'")
        log.debug("Removing old Twitter and Open Graph properties")
        html_modifier.remove_meta_properties(properties=OPEN_GRAPH_PROPERTIES)
        html_modifier.remove_meta_properties(properties=TWITTER_PROPERTIES)

        # Get all needed meta values
        title = page.meta.get(self.config.meta_keys.title_key, None)
        if title is not None and self.config.site_name_in_title.location == TitleLocationChoiceEnum.BEFORE:
            title = f"{config.site_name}{self.config.site_name_in_title.delimiter}{title}"
        elif title is not None and self.config.site_name_in_title.location == TitleLocationChoiceEnum.AFTER:
            title = f"{title}{self.config.site_name_in_title.delimiter}{config.site_name}"

        description = page.meta.get(self.config.meta_keys.description_key, None)

        image = page.meta.get(self.config.meta_keys.image_key, None)
        if image is not None:
            image = str(image)
            # TODO: use obsidian path link solver when it will be developed
            if image.startswith("../"):
                image = f"/{image.replace('../', '')}"
            if image.startswith("/"):
                image = image[1:]
            image_path = Path(config.docs_dir) / Path(image)
            if not image_path.exists():
                log.warning(
                    f"File: '{str(image)}' doesn't exists!\n"
                    f"('{self.config.meta_keys.image_key}' meta key"
                    f" from '{page.file.src_path}' file.)"
                )
            image = f'{config.site_url}{image.replace("//", "/")}'
        url = f"{config.site_url}{page.url}"
        site_name = config.site_name

        if self.config.og.enabled and title and description:
            log.debug("Adding Open Graph properties")
            html_modifier.add_meta_property(name="og:type", value="article")
            html_modifier.add_meta_property(name="og:title", value=title)
            html_modifier.add_meta_property(name="og:description", value=description)
            html_modifier.add_meta_property(name="og:site_name", value=site_name)
            html_modifier.add_meta_property(name="og:locale", value=self.config.og.locale)
            html_modifier.add_meta_property(name="og:url", value=url)

            if image is not None:
                html_modifier.add_meta_property(name="og:image", value=image)

        if self.config.twitter.enabled and title and description:
            log.debug("Adding Twitter/X properties")
            card_type = "summary_large_image" if image else "summary"
            html_modifier.add_meta_property(name="twitter:card", value=card_type)
            html_modifier.add_meta_property(name="twitter:title", value=title)
            html_modifier.add_meta_property(name="twitter:description", value=description)

            if image is not None:
                html_modifier.add_meta_property(name="twitter:image", value=image)

            if self.config.twitter.website:
                html_modifier.add_meta_property(name="twitter:site", value=self.config.twitter.website)

            if self.config.twitter.author:
                html_modifier.add_meta_property(name="twitter:creator", value=self.config.twitter.author)

        return str(html_modifier)
