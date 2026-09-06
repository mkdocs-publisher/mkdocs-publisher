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
import urllib.parse
from typing import Optional
from typing import Union

import pymdownx.slugs

from mkdocs_publisher.meta.config import SlugModeChoiceEnum

log = logging.getLogger("mkdocs.publisher._shared.links")


def slugify(text: str, keep_unicode: bool = False) -> str:
    """Text slugify function that produces the same slug as MkDocs one

    Non-ASCII characters are stripped (just like MkDocs does it), unless
    keep_unicode is set. It's a fallback for texts that consist of non-ASCII
    characters only, since those would be slugified into an empty string.
    """

    text = urllib.parse.unquote(text)
    if keep_unicode:
        return str(pymdownx.slugs.slugify(case="lower", normalize="NFC")(text=text, sep="-"))
    text = pymdownx.slugs.slugify(case="lower", normalize="NFD")(text=text, sep="-")
    return str(text).encode("ASCII", "ignore").decode("utf-8")


def create_slug(
    file_name: str,
    slug_mode: Union[SlugModeChoiceEnum, str],
    slug: Optional[str],
    title: Optional[str],
    warn_on_missing: bool = True,
) -> str:
    """Generate slug for various modes"""
    # When slug from meta key is not present, try to get slug value the other way
    if not slug or slug == "none":
        if slug_mode == SlugModeChoiceEnum.TITLE and title is not None:
            slug = slugify(text=title)
        elif slug_mode == SlugModeChoiceEnum.FILENAME:
            slug = slugify(text=file_name)

    # Log slug value
    if not slug or slug == "none":
        slug = slugify(text=file_name)

        if warn_on_missing and slug:
            log.warning(f'No slug for file "{file_name}" (mode: {slug_mode}). Fallback to file name.')

    # Slugification strips non-ASCII characters, so a title or a file name written
    # entirely in a non-latin alphabet ends up as an empty slug. Such a slug builds
    # an absolute destination path (like "/index.html"), which breaks a site build,
    # so original characters are kept instead (they are URL encoded later on).
    if not slug:
        slug = slugify(text=file_name, keep_unicode=True) or file_name

        if warn_on_missing:
            log.warning(
                f'Slug for file "{file_name}" has no ASCII characters. Fallback to a non-ASCII slug: "{slug}".'
            )

    log.debug(f'Slug for file "{file_name}" is: "{slug}"')
    return slug
