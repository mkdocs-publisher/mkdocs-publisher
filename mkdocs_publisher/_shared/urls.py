# MIT License
#
# Copyright (c) 2023 Maciej 'maQ' Kusz <maciej.kusz@gmail.com>
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
import urllib.parse
from typing import Optional
from typing import Union

import pymdownx.slugs

from mkdocs_publisher.meta.config import SlugModeEnum

log = logging.getLogger("mkdocs.plugins.publisher._shared.links")


def slugify(text: str) -> str:
    """Text slugify function that produces the same slug as MkDocs one"""

    text = urllib.parse.unquote(text)
    text = pymdownx.slugs.slugify(case="lower", normalize="NFD")(text=text, sep="-")
    return str(text).encode("ASCII", "ignore").decode("utf-8")


def create_slug(
    meta: dict,
    file_name: str,
    slug_mode: Union[SlugModeEnum, str],
    slug_key_name: str,
    title_key_name: str,
    warn_on_missing: bool = True,
) -> Optional[str]:
    """Generate slug for various modes"""
    slug = meta.get(slug_key_name)  # Slug meta key is always the most important

    # When slug meta key is not present, try to get slug value the other way
    if slug is None or slug == "none":
        if slug_mode == SlugModeEnum.TITLE:
            slug = slugify(text=str(meta.get(title_key_name)))
        elif slug_mode == SlugModeEnum.FILENAME:
            slug = slugify(text=file_name)

    # Log slug value
    if slug is None or slug == "none":
        slug = slugify(text=file_name)

        if warn_on_missing:
            log.warning(
                f'No slug for file "{file_name}" ' f"(mode: {slug_mode}). Fallback to file name."
            )

    log.debug(f'Slug for file "{file_name}" is: "{slug}"')
    return slug
