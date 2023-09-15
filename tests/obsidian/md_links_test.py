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
from pathlib import Path
from unittest.mock import patch

import pytest
from mkdocs.config.defaults import MkDocsConfig
from pytest import LogCaptureFixture

from mkdocs_publisher.blog.plugin import BlogPlugin
from mkdocs_publisher.obsidian import md_links
from mkdocs_publisher.obsidian.plugin import ObsidianPlugin


@pytest.mark.parametrize(
    "link,text,anchor,is_wiki,expected",
    {
        ("../file.md", "Link text", "", False, "[Link text](../file.md)"),
        ("../file", "Link text", "", True, "[Link text](../file.md)"),
        ("../file.md", "Link text", "anchor-value", False, "[Link text](../file.md#anchor-value)"),
        ("../file", "Link text", "anchor-value", True, "[Link text](../file.md#anchor-value)"),
    },
)
def test_link_match_dataclass(link: str, text: str, anchor: str, is_wiki: bool, expected: str):
    link_obj = md_links.LinkMatch(link=link, text=text, is_wiki=is_wiki, anchor=anchor)
    assert str(link_obj) == expected


@pytest.mark.parametrize(
    "link,image,anchor,extra,expected",
    {
        ("../image.jpg", "", "", "", "![image.jpg](../image.jpg)"),
        ("../image.jpg", "300", "", "", "![image.jpg](../image.jpg){width=300}"),
        ("../image.jpg", "300x300", "", "", "![image.jpg](../image.jpg){width=300 height=300}"),
        ("../image.jpg", "", "", "align=right", "![image.jpg](../image.jpg){align=right}"),
        (
            "../image.jpg",
            "300x300",
            "",
            "loading=lazy",
            "![image.jpg](../image.jpg){loading=lazy width=300 height=300}",
        ),
        ("../document.pdf", "", "", "", "![document.pdf](../document.pdf){pdfjs}"),
        ("../document.pdf", "", "page=3", "", "![document.pdf](../document.pdf){pdfjs page=3}"),
        (
            "../document.pdf",
            "",
            "height=300",
            "",
            "![document.pdf](../document.pdf){pdfjs height=300}",
        ),
    },
)
def test_wiki_embed_link_match_dataclass(
    link: str, image: str, anchor: str, extra: str, expected: str
):
    link_obj = md_links.WikiEmbedLinkMatch(link=link, image=image, anchor=anchor, extra=extra)
    assert str(link_obj) == expected


@pytest.mark.parametrize(
    "link,text,extra,is_loading_lazy,expected",
    {
        ("../image.jpg", "Description", "", False, "![Description](../image.jpg)"),
        (
            "../image.jpg",
            "Description",
            "align=right",
            False,
            "![Description](../image.jpg){align=right}",
        ),
        ("../image.jpg", "Description", "", True, "![Description](../image.jpg){loading=lazy}"),
        (
            "../image.jpg",
            "Description",
            "align=right",
            True,
            "![Description](../image.jpg){align=right loading=lazy}",
        ),
    },
)
def test_md_embed_link_match_dataclass(
    link: str, text: str, extra: str, is_loading_lazy: bool, expected: str
):
    link_obj = md_links.MdEmbedLinkMatch(
        link=link, text=text, extra=extra, is_loading_lazy=is_loading_lazy
    )
    assert str(link_obj) == expected


def test_relative_path_finder_properties(
    test_data_path: Path,
    relative_path_finder: md_links.RelativePathFinder,
):
    assert relative_path_finder.relative_path == Path("relative")
    assert relative_path_finder.current_file_path == Path("current/file.md")


def test_relative_path_finder_get_existing_file_path(
    test_data_path: Path,
    relative_path_finder: md_links.RelativePathFinder,
):
    file_path = relative_path_finder.get_full_file_path(file_path=Path("rel_file.md"))
    assert file_path == test_data_path / "relative/rel_file.md"


def test_relative_path_finder_get_existing_full_file_path(
    test_data_path: Path,
    relative_path_finder: md_links.RelativePathFinder,
):
    file_path = relative_path_finder.get_full_file_path(file_path=Path("relative/rel_file.md"))
    assert file_path == test_data_path / "relative/rel_file.md"


def test_relative_path_finder_get_non_existing_file_path(
    caplog: LogCaptureFixture,
    test_data_path: Path,
    relative_path_finder: md_links.RelativePathFinder,
):
    file_path = relative_path_finder.get_full_file_path(file_path=Path("non-existing.md"))
    assert file_path is None
    assert caplog.records[-1].levelno == logging.ERROR
    assert (
        caplog.records[-1].message == f'File: "non-existing.md" doesn\'t exists '
        f'(from: "{test_data_path}")'
    )


def test_relative_path_finder_get_non_existing_but_found_file_path(
    caplog: LogCaptureFixture,
    test_data_path: Path,
    relative_path_finder: md_links.RelativePathFinder,
):
    with patch.object(Path, "is_file") as mock_is_file:
        mock_is_file.return_value = False
        file_path = relative_path_finder.get_full_file_path(file_path=Path("rel_file.md"))
        assert file_path is None
        assert caplog.records[-1].levelno == logging.ERROR
        assert (
            caplog.records[-1].message == f'File: "rel_file.md" doesn\'t exists '
            f'(from: "{test_data_path}")'
        )


@pytest.mark.parametrize(
    "file_path,expected",
    {
        ("main.md", "../../main.md"),
        ("current/file.md", "../../current/file.md"),
        ("relative/rel_sub/rel_sub_file.md", "../rel_sub/rel_sub_file.md"),
        ("current/cur_sub/cur_sub_file.md", "../cur_sub/cur_sub_file.md"),
    },
)
def test_get_relative_file_path(
    file_path: str,
    expected: str,
    test_data_path: Path,
    relative_sub_path_finder: md_links.RelativePathFinder,
):
    file_path = str(
        relative_sub_path_finder.get_relative_file_path(file_path=test_data_path / file_path)
    )
    assert file_path == expected


@pytest.mark.parametrize(
    "link,text,anchor,expected",
    {
        ("main.md", "Main markdown", "", "[Main markdown](../main.md)"),
        ("main.md", "Main with anchor", "#anchor", "[Main with anchor](../main.md#anchor)"),
        ("#just-anchor", "Just Anchor", "", "[Just Anchor](#just-anchor)"),
        (
            "relative/other_rel_file.md",
            "Other markdown",
            "",
            "[Other markdown](other_rel_file.md)",
        ),
        ("relative/rel_sub/index-0.md", "Index 0", "", "[Index 0](rel_sub/index-0.md)"),
        ("relative/non_existing.md", "Non-existing", "", "[Non-existing]()"),
    },
)
def test_blog_link_match_dataclass(
    link: str,
    text: str,
    anchor: str,
    expected: str,
    relative_blog_path_finder: md_links.RelativePathFinder,
):
    link_obj = md_links.RelativeLinkMatch(link=link, text=text, anchor=anchor)
    link_obj.relative_path_finder = relative_blog_path_finder
    assert str(link_obj) == expected


@pytest.mark.parametrize(
    "link,text,anchor,expected",
    {
        (
            "current/cur_sub/cur_sub_file.md",
            "Sub markdown",
            "",
            "[Sub markdown](current/cur_sub/cur_sub_file.md)",
        ),
        (
            "current/cur_sub/cur_sub_file.md",
            "Sub markdown",
            "anchor",
            "[Sub markdown](current/cur_sub/cur_sub_file.md#anchor)",
        ),
    },
)
def test_relative_link_match_dataclass(
    link: str,
    text: str,
    anchor: str,
    expected: str,
    relative_path_finder: md_links.RelativePathFinder,
):
    link_obj = md_links.RelativeLinkMatch(link=link, text=text, anchor=anchor)
    link_obj.relative_path_finder = relative_path_finder
    assert str(link_obj) == expected


@pytest.mark.parametrize(
    "markdown,expected",
    {
        (
            "Lorem ipsum dolor sit [[file|amet]], consectetur adipiscing elit.",
            "Lorem ipsum dolor sit [amet](file.md), consectetur adipiscing elit.",
        ),
        (
            "Lorem ipsum dolor sit ![[amet.pdf]], consectetur adipiscing elit.",
            "Lorem ipsum dolor sit ![amet.pdf](amet.pdf){pdfjs loading=lazy}, "
            "consectetur adipiscing elit.",
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
    mkdocs_config.plugins = {"pub-obsidian": pub_obsidian_plugin, "pub-blog": pub_blog_plugin}  # type: ignore
    markdown_links = md_links.MarkdownLinks(mkdocs_config=mkdocs_config)
    markdown = markdown_links.normalize_links(markdown=markdown, current_file_path="main.md")
    assert markdown == expected


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
    mkdocs_config.plugins = {"pub-obsidian": pub_obsidian_plugin, "pub-blog": pub_blog_plugin}  # type: ignore
    markdown_links = md_links.MarkdownLinks(mkdocs_config=mkdocs_config)
    markdown = markdown_links.normalize_links(markdown=markdown, current_file_path="main.md")
    assert markdown == expected


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
@pytest.mark.parametrize(
    "mkdocs_config",
    [{"docs_dir": "tests/obsidian/tests_data"}],
    indirect=True,
)
def test_normalize_relative_links(
    markdown: str,
    expected: str,
    mkdocs_config: MkDocsConfig,
    pub_obsidian_plugin: ObsidianPlugin,
    pub_blog_plugin: BlogPlugin,
):
    mkdocs_config.plugins = {"pub-obsidian": pub_obsidian_plugin, "pub-blog": pub_blog_plugin}  # type: ignore
    logging.error(mkdocs_config)
    markdown_links = md_links.MarkdownLinks(mkdocs_config=mkdocs_config)
    markdown = markdown_links.normalize_relative_links(
        markdown=markdown, current_file_path="current/cur_sub/cur_sub_file.md"
    )
    assert markdown == expected
