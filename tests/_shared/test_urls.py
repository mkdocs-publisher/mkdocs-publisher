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

import pytest
from pytest import LogCaptureFixture

from mkdocs_publisher._shared import urls
from mkdocs_publisher.meta.config import SlugModeChoiceEnum


@pytest.mark.parametrize(
    "text,expected",
    {
        ("lorem ipsum dolor", "lorem-ipsum-dolor"),
        ("lorem_ipsum_dolor", "lorem_ipsum_dolor"),
        ("ąćęłńóśżź", "acenoszz"),
        ("Lorem ipsum, dolor", "lorem-ipsum-dolor"),
    },
)
def test_slugify(text, expected):
    assert expected == urls.slugify(text)


@pytest.mark.parametrize(
    "slug,title,slug_mode,warn_on_missing,expected,exp_log_level",
    {
        (
            "meta_slug",
            "title_slug",
            SlugModeChoiceEnum.TITLE.name,
            False,
            "meta_slug",
            logging.DEBUG,
        ),
        (None, "title_slug", SlugModeChoiceEnum.TITLE.name, False, "title_slug", logging.DEBUG),
        (
            "meta_slug",
            "title_slug",
            SlugModeChoiceEnum.FILENAME.name,
            False,
            "meta_slug",
            logging.DEBUG,
        ),
        (None, None, SlugModeChoiceEnum.FILENAME.name, False, "file_name_slug", logging.DEBUG),
        (None, None, SlugModeChoiceEnum.TITLE.name, True, "file_name_slug", logging.WARNING),
        (None, None, SlugModeChoiceEnum.TITLE.name, False, "file_name_slug", logging.DEBUG),
        (None, None, None, False, "file_name_slug", logging.DEBUG),
    },
)
def test_slug_create(
    caplog: LogCaptureFixture,
    slug: str,
    title: str,
    slug_mode: str,
    warn_on_missing: bool,
    expected: str,
    exp_log_level: int,
):
    assert expected == urls.create_slug(
        file_name="file_name_slug",
        slug_mode=slug_mode,
        slug=slug,
        title=title,
        warn_on_missing=warn_on_missing,
    )

    assert exp_log_level == caplog.records[0].levelno
