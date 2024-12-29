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

from pathlib import Path
from unittest.mock import patch

import pytest
from mkdocs.config.defaults import MkDocsConfig
from pytest_check import check_functions as check

from mkdocs_publisher.meta.meta_files import MetaFile
from mkdocs_publisher.meta.meta_nav import MetaNav


def test_nav_no_files(patched_meta_nav: MetaNav, mkdocs_config: MkDocsConfig):
    check.is_false(patched_meta_nav.build_nav(mkdocs_config=mkdocs_config), "To much files")


def test_nav_basic_structure(patched_meta_nav: MetaNav, mkdocs_config: MkDocsConfig):
    parent_dir: MetaFile = MetaFile(
        path=Path("fake_dir"),
        abs_path=Path("docs/fake_dir"),
        is_dir=True,
    )
    parent_dir.title = "Fake dir"
    patched_meta_nav._meta_files["fake_dir"] = parent_dir

    sub_file: MetaFile = MetaFile(
        path=Path("fake_dir/fake_sub_file.md"),
        abs_path=Path("docs/fake_dir/fake_sub_file.md"),
        is_dir=False,
    )
    sub_file.title = "Fake title sub"
    sub_file.is_draft = False
    patched_meta_nav._meta_files["fake_dir/fake_sub_file.md"] = sub_file

    file: MetaFile = MetaFile(
        path=Path("fake_file.md"),
        abs_path=Path("docs/fake_file.md"),
        is_dir=False,
    )
    file.title = "Fake title"
    file.is_draft = False
    patched_meta_nav._meta_files["fake_file.md"] = file

    other_parent_dir: MetaFile = MetaFile(
        path=Path("other_fake_dir"),
        abs_path=Path("docs/other_fake_dir"),
        is_dir=True,
    )
    other_parent_dir.title = "Other fake dir"
    patched_meta_nav._meta_files["other_fake_dir"] = other_parent_dir

    other_sub_file: MetaFile = MetaFile(
        path=Path("other_fake_dir/fake_sub_file.md"),
        abs_path=Path("docs/other_fake_dir/fake_sub_file.md"),
        is_dir=False,
    )
    other_sub_file.title = "Fake title sub"
    other_sub_file.is_draft = False
    patched_meta_nav._meta_files["other_fake_dir/fake_sub_file.md"] = other_sub_file

    nav = patched_meta_nav.build_nav(mkdocs_config=mkdocs_config)

    check.equal(
        nav,
        [
            {"fake_dir": [{"Fake title sub": "fake_dir/fake_sub_file.md"}]},
            {"Fake title": "fake_file.md"},
            {"other_fake_dir": [{"Fake title sub": "other_fake_dir/fake_sub_file.md"}]},
        ],
        "wrong",
    )


def test_nav_with_blog_dir(patched_meta_nav: MetaNav, mkdocs_config: MkDocsConfig):
    parent_meta_file: MetaFile = MetaFile(
        path=Path("blog"),
        abs_path=Path("docs/blog"),
        is_dir=False,
    )
    parent_meta_file.title = "Blog dir"
    parent_meta_file.is_dir = True
    patched_meta_nav._meta_files["blog"] = parent_meta_file

    meta_file: MetaFile = MetaFile(
        path=Path("blog/fake_file.md"),
        abs_path=Path("docs/blog/fake_file.md"),
        is_dir=False,
    )
    meta_file.title = "Fake title"
    meta_file.is_draft = False
    meta_file.is_overview = False
    patched_meta_nav._meta_files["blog/fake_file.md"] = meta_file

    nav = patched_meta_nav.build_nav(mkdocs_config=mkdocs_config)

    check.equal(nav, [{"blog": "blog"}], "Blog dir error")


@pytest.mark.parametrize(
    "redirect,expected",
    [
        ("other_fake_file.md", "fake_file.md"),
        ("https://fake_url.com/", "https://fake_url.com/"),
    ],
)
def test_nav_redirect(patched_meta_nav: MetaNav, mkdocs_config: MkDocsConfig, redirect: str, expected: str):
    meta_file: MetaFile = MetaFile(
        path=Path("fake_file.md"),
        abs_path=Path("docs/fake_file.md"),
        is_dir=False,
    )
    meta_file.title = "Fake title"
    meta_file.is_draft = False
    meta_file.redirect = redirect
    patched_meta_nav._meta_files["fake_file.md"] = meta_file

    nav = patched_meta_nav.build_nav(mkdocs_config=mkdocs_config)

    check.equal(nav, [{"Fake title": expected}], "Redirect error")


@pytest.mark.parametrize(
    "file_name,is_draft,is_hidden,expected",
    [
        ("fake_file.txt", False, False, []),
        ("fake_file.md", True, False, []),
        ("fake_file.md", False, True, [{"Fake title": "fake_file.md"}]),
    ],
)
def test_nav_by_publication_status(
    patched_meta_nav: MetaNav,
    mkdocs_config: MkDocsConfig,
    file_name: str,
    is_draft: bool,
    is_hidden: bool,
    expected: list,
):
    meta_file: MetaFile = MetaFile(
        path=Path(file_name),
        abs_path=Path(f"docs/{file_name}"),
        is_dir=False,
    )
    meta_file.title = "Fake title"
    meta_file.is_draft = is_draft
    meta_file.is_hidden = is_hidden
    patched_meta_nav._meta_files[file_name] = meta_file

    nav = patched_meta_nav.build_nav(mkdocs_config=mkdocs_config)

    check.equal(nav, expected, "Publication status error")


@pytest.mark.parametrize(
    "is_overview,expected",
    [
        (True, [{"fake_dir": ["fake_dir/README.md", {"Fake title sub": "fake_dir/fake_sub_file.md"}]}]),
        (False, [{"fake_dir": [{"Fake title sub": "fake_dir/fake_sub_file.md"}]}]),
    ],
)
def test_nav_overview(patched_meta_nav: MetaNav, mkdocs_config: MkDocsConfig, is_overview, expected: list):
    def patched_get_overview_nav(meta_file: MetaFile) -> list[str]:
        return [str(meta_file.path.joinpath("README.md"))]

    parent_dir: MetaFile = MetaFile(
        path=Path("fake_dir"),
        abs_path=Path("docs/fake_dir"),
        is_dir=True,
    )
    parent_dir.title = "Fake dir"
    parent_dir.is_overview = is_overview
    patched_meta_nav._meta_files["fake_dir"] = parent_dir

    if is_overview:
        patched_meta_nav._get_overview_nav = patched_get_overview_nav

    sub_file: MetaFile = MetaFile(
        path=Path("fake_dir/fake_sub_file.md"),
        abs_path=Path("docs/fake_dir/fake_sub_file.md"),
        is_dir=False,
    )
    sub_file.title = "Fake title sub"
    sub_file.is_draft = False
    patched_meta_nav._meta_files["fake_dir/fake_sub_file.md"] = sub_file

    nav = patched_meta_nav.build_nav(mkdocs_config=mkdocs_config)

    check.equal(nav, expected, "Overview error")


@pytest.mark.parametrize("is_relative_to", [(True), (False)])
def test_nav_empty_relative_dir(patched_meta_nav: MetaNav, mkdocs_config: MkDocsConfig, is_relative_to: bool):
    parent_dir: MetaFile = MetaFile(
        path=Path("fake_dir"),
        abs_path=Path("docs/fake_dir"),
        is_dir=True,
    )
    parent_dir.title = "Fake dir"
    parent_dir.is_draft = False
    patched_meta_nav._meta_files["fake_dir"] = parent_dir

    with patch.object(Path, "is_relative_to", return_value=is_relative_to):
        nav = patched_meta_nav.build_nav(mkdocs_config=mkdocs_config)

    check.equal(nav, [], "Empty relative dir error")
