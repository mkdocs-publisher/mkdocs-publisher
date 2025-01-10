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
import pytest
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.structure.files import File
from mkdocs.structure.nav import Link
from mkdocs.structure.nav import Section
from mkdocs.structure.pages import Page
from pytest_check import check_functions as check

from mkdocs_publisher.meta.meta_nav import MetaNav


@pytest.mark.parametrize(
    "removal_list,expected",
    [
        ([], True),
        (["fake_file.md"], False),
        (["fake_other_file.md"], True),
    ],
)
def test_nav_cleanup_for_page(
    mkdocs_config: MkDocsConfig,
    meta_nav: MetaNav,
    removal_list: list,
    expected: bool,
):
    page = Page(
        "Fake file",
        file=File(
            path="fake_file.md",
            src_dir="/Users/me",
            dest_dir="/Users/docs",
            use_directory_urls=True,
        ),
        config=mkdocs_config,
    )
    nav = meta_nav.nav_cleanup(
        items=[page],
        removal_list=removal_list,
    )
    check.equal(nav, [page] if expected else [])


@pytest.mark.parametrize(
    "removal_list,expected",
    [
        ([], True),
        (["Fake file"], False),
        (["Fake other file"], True),
    ],
)
def test_nav_cleanup_for_link(
    mkdocs_config: MkDocsConfig,
    meta_nav: MetaNav,
    removal_list: list,
    expected: bool,
):
    link = Link(title="Fake file", url="fake-file")
    nav = meta_nav.nav_cleanup(
        items=[link],
        removal_list=removal_list,
    )
    check.equal(nav, [link] if expected else [])


@pytest.mark.parametrize(
    "removal_list,expected",
    [
        ([], True),
        (["Fake file"], False),
        (["Some section"], True),
    ],
)
def test_nav_cleanup_for_section(
    mkdocs_config: MkDocsConfig,
    meta_nav: MetaNav,
    removal_list: list,
    expected: bool,
):
    link = Link(title="Fake file", url="fake-file")
    section = Section("Some section", children=[link])

    nav = meta_nav.nav_cleanup(
        items=[section],
        removal_list=removal_list,
    )
    check.equal(nav, [section] if expected else [])
