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

import pytest
from pytest import LogCaptureFixture

from mkdocs_publisher._shared import links


@pytest.mark.parametrize(
    "link,text,anchor,title,is_wiki,expected",
    {
        ("../file.md", "Link text", "", "", False, "[Link text](../file.md)"),
        (
            "../file with space.md",
            "Link text",
            "",
            "",
            False,
            "[Link text](../file with space.md)",
        ),
        ("../file", "Link text", "", "", True, "[Link text](../file.md)"),
        (
            "../file.md",
            "Link text",
            "anchor-value",
            "",
            False,
            "[Link text](../file.md#anchor-value)",
        ),
        ("../file", "Link text", "anchor-value", "", True, "[Link text](../file.md#anchor-value)"),
        (
            "../file.md",
            "Link text",
            "anchor-value",
            "title value",
            False,
            '[Link text](../file.md#anchor-value "title value")',
        ),
        (
            "../file",
            "Link text",
            "anchor-value",
            "title value",
            True,
            '[Link text](../file.md#anchor-value "title value")',
        ),
        (
            "../file.md",
            "Link text",
            "",
            "title value",
            False,
            '[Link text](../file.md "title value")',
        ),
        (
            "../file",
            "Link text",
            "",
            "title value",
            True,
            '[Link text](../file.md "title value")',
        ),
        (
            None,
            "Anchor link",
            "just/an anchor",
            "",
            False,
            "[Anchor link](#just/an anchor)",
        ),
    },
)
def test_link_match_dataclass(
    link: str, text: str, anchor: str, title: str, is_wiki: bool, expected: str
):
    link_obj = links.LinkMatch(link=link, text=text, title=title, is_wiki=is_wiki, anchor=anchor)
    assert expected == str(link_obj)


@pytest.mark.parametrize(
    "link,image,anchor,extra,expected",
    {
        ("../image.jpg", "", "", "", "![image.jpg](../image.jpg)"),
        (
            "../image with space.jpg",
            "",
            "",
            "",
            "![image with space.jpg](../image with space.jpg)",
        ),
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
    link_obj = links.WikiEmbedLinkMatch(link=link, image=image, anchor=anchor, extra=extra)
    assert expected == str(link_obj)


@pytest.mark.parametrize(
    "link,text,title,extra,is_loading_lazy,expected",
    {
        ("../image.jpg", "Description", "", "", False, "![Description](../image.jpg)"),
        (
            "../image with space.jpg",
            "Description",
            "",
            "",
            False,
            "![Description](../image with space.jpg)",
        ),
        (
            "../image.jpg",
            "Description",
            "",
            "align=right",
            False,
            "![Description](../image.jpg){align=right}",
        ),
        (
            "../image.jpg",
            "Description",
            "",
            "",
            True,
            "![Description](../image.jpg){loading=lazy}",
        ),
        (
            "../image.jpg",
            "Description",
            "",
            "align=right",
            True,
            "![Description](../image.jpg){align=right loading=lazy}",
        ),
        (
            "../image.jpg",
            "Description",
            "title value",
            "",
            False,
            '![Description](../image.jpg "title value")',
        ),
        (
            "../image.jpg",
            "Description",
            "title value",
            "align=right",
            False,
            '![Description](../image.jpg "title value"){align=right}',
        ),
        (
            "../image.jpg",
            "Description",
            "title value",
            "align=right",
            True,
            '![Description](../image.jpg "title value"){align=right loading=lazy}',
        ),
    },
)
def test_md_embed_link_match_dataclass(
    link: str, text: str, title: str, extra: str, is_loading_lazy: bool, expected: str
):
    link_obj = links.MdEmbedLinkMatch(
        link=link, text=text, title=title, extra=extra, is_loading_lazy=is_loading_lazy
    )
    assert expected == str(link_obj)


def test_relative_path_finder_properties(
    relative_path_finder: links.RelativePathFinder,
):
    assert Path("relative") == relative_path_finder.relative_path
    assert Path("current/file.md") == relative_path_finder.current_file_path


def test_relative_path_finder_get_existing_file_path(
    test_data_dir: Path,
    relative_path_finder: links.RelativePathFinder,
):
    file_path = relative_path_finder.get_full_file_path(file_path=Path("rel_file.md"))
    assert test_data_dir / "relative/rel_file.md" == file_path


def test_relative_path_finder_get_existing_full_file_path(
    test_data_dir: Path,
    relative_path_finder: links.RelativePathFinder,
):
    file_path = relative_path_finder.get_full_file_path(file_path=Path("relative/rel_file.md"))
    assert test_data_dir / "relative/rel_file.md" == file_path


def test_relative_path_finder_get_non_existing_file_path(
    caplog: LogCaptureFixture,
    test_data_dir: Path,
    relative_path_finder: links.RelativePathFinder,
):
    file_path = relative_path_finder.get_full_file_path(file_path=Path("non-existing.md"))
    assert file_path is None
    assert caplog.records[-1].levelno == logging.ERROR
    assert (
        f'File: "non-existing.md" doesn\'t exists (from: "{test_data_dir}")'
        == caplog.records[-1].message
    )


def test_relative_path_finder_multiple_file_found(
    caplog: LogCaptureFixture,
    relative_path_finder: links.RelativePathFinder,
):
    file_path = relative_path_finder.get_full_file_path(file_path=Path("other_rel_file.md"))
    assert file_path is None
    assert caplog.records[-1].levelno == logging.ERROR
    assert (
        caplog.records[-1].message == "Too much files found: ['relative/other_rel_file.md', "
        "'current/cur_sub/other_rel_file.md']"
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
    test_data_dir: Path,
    relative_sub_path_finder: links.RelativePathFinder,
):
    file_path = str(
        relative_sub_path_finder.get_relative_file_path(file_path=test_data_dir / file_path)
    )
    assert expected == file_path


@pytest.mark.parametrize(
    "link,text,anchor,title,expected",
    {
        ("main.md", "Main markdown", "", "", "[Main markdown](../main.md)"),
        ("main.md", "Main with anchor", "anchor", "", "[Main with anchor](../main.md#anchor)"),
        (
            "main.md",
            "Main with anchor",
            "anchor",
            "title",
            '[Main with anchor](../main.md#anchor "title")',
        ),
        ("#just-anchor", "Just Anchor", "", "", "[Just Anchor](#just-anchor)"),
        (
            "relative/other_rel_file.md",
            "Other markdown",
            "",
            "",
            "[Other markdown](other_rel_file.md)",
        ),
        ("relative/rel_sub/index-0.md", "Index 0", "", "", "[Index 0](rel_sub/index-0.md)"),
        ("relative/non_existing.md", "Non-existing", "", "", "[Non-existing]()"),
    },
)
def test_blog_link_match_dataclass(
    link: str,
    text: str,
    anchor: str,
    title: str,
    expected: str,
    relative_blog_path_finder: links.RelativePathFinder,
):
    link_obj = links.RelativeLinkMatch(link=link, text=text, anchor=anchor, title=title)
    link_obj.relative_path_finder = relative_blog_path_finder
    assert expected == str(link_obj)


@pytest.mark.parametrize(
    "link,text,anchor,title,expected",
    {
        (
            "current/cur_sub/cur_sub_file.md",
            "Sub markdown",
            "",
            "",
            "[Sub markdown](current/cur_sub/cur_sub_file.md)",
        ),
        (
            "current/cur_sub/cur_sub_file.md",
            "Sub markdown",
            "anchor",
            "",
            "[Sub markdown](current/cur_sub/cur_sub_file.md#anchor)",
        ),
        (
            "current/cur_sub/cur_sub_file.md",
            "Sub markdown",
            "",
            "title",
            '[Sub markdown](current/cur_sub/cur_sub_file.md "title")',
        ),
        (
            "current/cur_sub/cur_sub_file.md",
            "Sub markdown",
            "anchor",
            "title",
            '[Sub markdown](current/cur_sub/cur_sub_file.md#anchor "title")',
        ),
    },
)
def test_relative_link_match_dataclass(
    link: str,
    text: str,
    anchor: str,
    title: str,
    expected: str,
    relative_path_finder: links.RelativePathFinder,
):
    link_obj = links.RelativeLinkMatch(link=link, text=text, anchor=anchor, title=title)
    link_obj.relative_path_finder = relative_path_finder
    assert expected == str(link_obj)
