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

from pathlib import Path
from typing import cast

import pytest
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.plugins import PluginCollection
from pytest_check import check_functions as check

from mkdocs_publisher.blog.plugin import BlogPlugin
from mkdocs_publisher.obsidian import md_links
from mkdocs_publisher.obsidian.plugin import ObsidianPlugin


@pytest.mark.parametrize(
    "markdown,expected",
    {
        (
            "Lorem ipsum dolor [sit](file.md) amet, consectetur adipiscing elit.",
            "Lorem ipsum dolor [sit](file.md) amet, consectetur adipiscing elit.",
        ),
        (
            "Lorem ipsum dolor [sit](file with space.md) amet, consectetur adipiscing elit.",
            "Lorem ipsum dolor [sit](file with space.md) amet, consectetur adipiscing elit.",
        ),
        (
            "Lorem ipsum dolor sit [amet](file.md#anchor part), consectetur adipiscing elit.",
            "Lorem ipsum dolor sit [amet](file.md#anchor-part), consectetur adipiscing elit.",
        ),
        (
            'Lorem ipsum dolor sit [amet](file.md "title"), consectetur adipiscing elit.',
            'Lorem ipsum dolor sit [amet](file.md "title"), consectetur adipiscing elit.',
        ),
        (
            'Lorem ipsum dolor sit [amet](file.md#anchor part "title"), consectetur adipiscing elit.',
            'Lorem ipsum dolor sit [amet](file.md#anchor-part "title"), consectetur adipiscing elit.',
        ),
        (
            "Lorem ipsum dolor sit [amet](#just/an anchor), consectetur adipiscing elit.",
            "Lorem ipsum dolor sit [amet](#justan-anchor), consectetur adipiscing elit.",
        ),
        (
            "Lorem ipsum dolor sit [[file]] amet, consectetur adipiscing elit.",
            "Lorem ipsum dolor sit [file](file.md) amet, consectetur adipiscing elit.",
        ),
        (
            "Lorem ipsum dolor sit [[file]]{ .some .extra } amet, consectetur adipiscing elit.",
            "Lorem ipsum dolor sit [file](file.md){.some .extra} amet, consectetur adipiscing elit.",
        ),
        (
            "Lorem ipsum dolor sit [[file with space]] amet, consectetur adipiscing elit.",
            "Lorem ipsum dolor sit [file with space](file with space.md) amet, consectetur adipiscing elit.",
        ),
        (
            "Lorem ipsum dolor sit [[file with space]]{ .extra } amet, consectetur adipiscing elit.",
            "Lorem ipsum dolor sit [file with space](file with space.md){.extra} amet, consectetur adipiscing elit.",
        ),
        (
            "Lorem ipsum dolor sit amet [[#anchor part]], consectetur adipiscing elit.",
            "Lorem ipsum dolor sit amet [anchor part](#anchor-part), consectetur adipiscing elit.",
        ),
        (
            "Lorem ipsum dolor sit amet [[file#anchor part]], consectetur adipiscing elit.",
            "Lorem ipsum dolor sit amet [file > anchor part](file.md#anchor-part), consectetur adipiscing elit.",
        ),
        (
            "Lorem ipsum dolor sit [[file|amet]], consectetur adipiscing elit.",
            "Lorem ipsum dolor sit [amet](file.md), consectetur adipiscing elit.",
        ),
        (
            "Lorem ipsum dolor sit [[file with space|amet]], consectetur adipiscing elit.",
            "Lorem ipsum dolor sit [amet](file with space.md), consectetur adipiscing elit.",
        ),
        (
            "Lorem ipsum dolor sit ![[amet.pdf]], consectetur adipiscing elit.",
            "Lorem ipsum dolor sit ![amet.pdf](amet.pdf){pdfjs loading=lazy}, consectetur adipiscing elit.",
        ),
        (
            "Lorem ipsum dolor sit ![[amet.pdf]]{ .extra }, consectetur adipiscing elit.",
            "Lorem ipsum dolor sit ![amet.pdf](amet.pdf){.extra pdfjs loading=lazy}, consectetur adipiscing elit.",
        ),
        (
            "Lorem ipsum dolor sit [amet](file.md), consectetur adipiscing ![elit](elit.jpg).",
            "Lorem ipsum dolor sit [amet](file.md), consectetur adipiscing ![elit](elit.jpg){loading=lazy}.",
        ),
        (
            "Lorem ipsum dolor sit [amet](https://test.it/), consectetur adipiscing ![elit](elit.jpg).",
            "Lorem ipsum dolor sit [amet](https://test.it/), consectetur adipiscing ![elit](elit.jpg){loading=lazy}.",
        ),
    },
)
def test_normalize_wiki_links(
    markdown: str,
    expected: str,
    mkdocs_config: MkDocsConfig,
    pub_obsidian_plugin: ObsidianPlugin,
    pub_blog_plugin: BlogPlugin,
):
    mkdocs_config.plugins = cast(PluginCollection, {"pub-obsidian": pub_obsidian_plugin, "pub-blog": pub_blog_plugin})
    markdown_links = md_links.MarkdownLinks(mkdocs_config=mkdocs_config)
    markdown = markdown_links.normalize_links(markdown=markdown, current_file_path=Path("main.md"))

    check.equal(expected, markdown, "Wrong wiki link to markdown link")


@pytest.mark.parametrize(
    "markdown,expected",
    {
        (
            "Lorem ipsum dolor sit [[file|amet]], consectetur adipiscing elit.",
            "Lorem ipsum dolor sit [[file|amet]], consectetur adipiscing elit.",
        ),
        (
            "Lorem ipsum dolor sit ![[amet.pdf]], consectetur adipiscing elit.",
            "Lorem ipsum dolor sit ![[amet.pdf]], consectetur adipiscing elit.",
        ),
        (
            "Lorem ipsum dolor sit [amet](file.md), consectetur adipiscing elit.",
            "Lorem ipsum dolor sit [amet](file.md), consectetur adipiscing elit.",
        ),
        (
            "Lorem ipsum dolor sit ![amet](main.md), consectetur adipiscing elit.",
            "Lorem ipsum dolor sit ![amet](main.md){loading=lazy}, consectetur adipiscing elit.",
        ),
    },
)
def test_normalize_links(
    markdown: str,
    expected: str,
    mkdocs_config: MkDocsConfig,
    pub_obsidian_plugin: ObsidianPlugin,
    pub_blog_plugin: BlogPlugin,
):
    pub_obsidian_plugin.config.links.wikilinks_enabled = False
    mkdocs_config.plugins = cast(PluginCollection, {"pub-obsidian": pub_obsidian_plugin, "pub-blog": pub_blog_plugin})
    markdown_links = md_links.MarkdownLinks(mkdocs_config=mkdocs_config)
    markdown = markdown_links.normalize_links(markdown=markdown, current_file_path=Path("main.md"))

    check.equal(expected, markdown, "Wrong markdown link to markdown link")


@pytest.mark.parametrize(
    "markdown,expected",
    {
        (
            "Lorem ipsum dolor sit [amet](main.md), consectetur adipiscing elit.",
            "Lorem ipsum dolor sit [amet](main.md), consectetur adipiscing elit.",
        ),
        (
            "Lorem ipsum dolor sit ![amet](main.md), consectetur adipiscing elit.",
            "Lorem ipsum dolor sit ![amet](main.md), consectetur adipiscing elit.",
        ),
    },
)
def test_normalize_relative_links(
    markdown: str,
    expected: str,
    mkdocs_config: MkDocsConfig,
    pub_obsidian_plugin: ObsidianPlugin,
    pub_blog_plugin: BlogPlugin,
):
    mkdocs_config.plugins = cast(PluginCollection, {"pub-obsidian": pub_obsidian_plugin, "pub-blog": pub_blog_plugin})
    markdown_links = md_links.MarkdownLinks(mkdocs_config=mkdocs_config)
    markdown = markdown_links.normalize_relative_links(
        markdown=markdown,
        current_file_path=Path("main.md"),
        current_relative_path=Path("main.md"),
    )

    # TODO: is this test valid
    check.equal(expected, markdown, "Wrong relative link to markdown link")
