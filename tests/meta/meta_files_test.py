# MIT License
#
# Copyright (c) 2024 Maciej 'maQ' Kusz <maciej.kusz@gmail.com>
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

import pytest
from mkdocs.config.defaults import MkDocsConfig
from pytest import LogCaptureFixture

from meta.meta_files import MetaFile
from meta.meta_files import MetaFiles
from mkdocs_publisher.meta.plugin import MetaPlugin


@pytest.mark.parametrize(
    "path,abs_path,expected_name,expected_parent",
    [
        (
            Path("docs/fake_file.md"),
            Path("/Users/me/docs/fake_file.md"),
            "fake_file.md",
            Path("docs"),
        ),
        (
            Path("fake_file.md"),
            Path("/Users/me/docs/fake_file.md"),
            "fake_file.md",
            None,
        ),
    ],
)
def test_meta_files_properties(
    path: Path, abs_path: Path, expected_name: str, expected_parent: str
):
    meta_file = MetaFile(path=path, abs_path=abs_path, is_dir=False)
    assert meta_file.name == expected_name
    assert meta_file.parent == expected_parent


@pytest.mark.parametrize(
    "pub_meta_plugin,meta,markdown,is_dir,expected",
    [
        ({}, {}, "", False, False),  # File
        ({}, {}, "", True, False),  # Auto without text
        ({}, {}, "Some text", True, True),  # Auto with text
        ({}, {"overview": True}, "", True, True),  # Auto with override without text
        ({}, {"overview": True}, "Some text", True, True),  # Auto with override with text
        ({}, {"overview": False}, "Some text", True, False),  # Auto with override with text
        ({"overview": {"default": False}}, {}, "", False, False),
        ({"overview": {"default": False}}, {}, "", True, False),
        ({"overview": {"default": False}}, {"overview": True}, "", False, False),
        ({"overview": {"default": False}}, {"overview": True}, "", True, True),
        ({"overview": {"default": False}}, {"overview": False}, "", True, False),
        ({"overview": {"default": True}}, {}, "", False, False),
        ({"overview": {"default": True}}, {}, "", True, True),
        ({"overview": {"default": True}}, {"overview": True}, "", False, False),
        ({"overview": {"default": True}}, {"overview": True}, "", True, True),
        ({"overview": {"default": True}}, {"overview": False}, "", True, False),
        ({"overview": {"default": False, "key_name": "ov"}}, {"overview": True}, "", True, False),
        ({"overview": {"default": False, "key_name": "ov"}}, {"ov": True}, "", True, True),
    ],
    indirect=["pub_meta_plugin"],
)
def test_meta_files_overview(
    mkdocs_config: MkDocsConfig,
    pub_meta_plugin: MetaPlugin,
    meta: dict,
    markdown: str,
    is_dir: bool,
    expected: bool,
):
    meta_file: MetaFile = MetaFile(
        path=Path("fake_file.md"), abs_path=Path("/Users/me/docs/fake_file.md"), is_dir=is_dir
    )

    meta_files: MetaFiles = MetaFiles()
    meta_files.set_configs(mkdocs_config=mkdocs_config, meta_plugin_config=pub_meta_plugin.config)
    meta_files._get_overview(meta_file=meta_file, meta=meta, markdown=markdown)

    assert meta_file.is_overview is expected


@pytest.mark.parametrize(
    "pub_meta_plugin,meta,markdown,is_dir,expected,warn",
    [
        ({}, {"title": "Some title"}, "", False, "Some title", None),
        ({}, {"title": "Some title"}, "", True, "Some title", None),
        (
            {},
            {},
            "# Title",
            False,
            "Title",
            'Title value from "title" meta data is missing for file: "fake_file.md"',
        ),
        (
            {},
            {},
            "",
            False,
            "Fake File",
            'Title value from first heading is missing for file: "fake_file.md"',
        ),
        (
            {"title": {"warn_on_missing_meta": False}},
            {},
            "# Title",
            False,
            "Title",
            None,
        ),
        (
            {"title": {"warn_on_missing_header": False}},
            {},
            "",
            False,
            "Fake File",
            None,
        ),
        (
            {"title": {"mode": "head"}},
            {},
            "# Title",
            False,
            "Title",
            None,
        ),
    ],
    indirect=["pub_meta_plugin"],
)
def test_meta_files_title(
    mkdocs_config: MkDocsConfig,
    pub_meta_plugin: MetaPlugin,
    meta: dict,
    markdown: str,
    is_dir: bool,
    expected: str,
    warn: Optional[str],
    caplog: LogCaptureFixture,
):
    meta_file: MetaFile = MetaFile(
        path=Path("fake_file.md"), abs_path=Path("/Users/me/docs/fake_file.md"), is_dir=is_dir
    )

    meta_files: MetaFiles = MetaFiles()
    meta_files.set_configs(mkdocs_config=mkdocs_config, meta_plugin_config=pub_meta_plugin.config)
    meta_files._get_title(meta_file=meta_file, meta=meta, markdown=markdown)

    assert meta_file.title == expected
    if warn is not None:
        assert caplog.records[-1].levelno == logging.WARNING
        assert warn == caplog.records[-1].message


@pytest.mark.parametrize(
    "pub_meta_plugin,expect",
    [
        ({}, ["README.md", "index.md"]),
        ({"dir_meta_file": "any.md"}, ["README.md", "index.md", "any.md"]),
    ],
    indirect=["pub_meta_plugin"],
)
def test_meta_files_meta_file(
    mkdocs_config: MkDocsConfig,
    pub_meta_plugin: MetaPlugin,
    expect: list[str],
):
    meta_files: MetaFiles = MetaFiles()
    meta_files.set_configs(mkdocs_config=mkdocs_config, meta_plugin_config=pub_meta_plugin.config)
    assert meta_files.meta_files == expect


def test_meta_files_on_serve(mkdocs_config: MkDocsConfig, pub_meta_plugin: MetaPlugin):
    meta_files: MetaFiles = MetaFiles()
    meta_files.set_configs(mkdocs_config=mkdocs_config, meta_plugin_config=pub_meta_plugin.config)

    meta_files.on_serve = True
    assert meta_files.on_serve


@pytest.mark.parametrize(
    "mkdocs_config,hidden_path,expected",
    [
        ({"docs_dir": "docs"}, None, []),
        ({"docs_dir": "docs"}, Path("docs/hidden_dir"), [Path("hidden_dir")]),
    ],
    indirect=["mkdocs_config"],
)
def test_meta_files_add_hidden(
    mkdocs_config: MkDocsConfig,
    pub_meta_plugin: MetaPlugin,
    hidden_path: Optional[Path],
    expected: list,
):
    meta_files: MetaFiles = MetaFiles()
    meta_files.set_configs(mkdocs_config=mkdocs_config, meta_plugin_config=pub_meta_plugin.config)

    meta_files.add_hidden_path(hidden_path=hidden_path)

    assert meta_files._hidden_paths == expected


# def test_meta_files_hidden_files_and_paths(
#     mkdocs_config: MkDocsConfig, pub_meta_plugin: MetaPlugin
# ):
#     meta_files: MetaFiles = MetaFiles()
#     meta_files.set_configs(
#         mkdocs_config=mkdocs_config, meta_plugin_config=pub_meta_plugin.config
#     )
#
#     for i in range(5):
#         is_dir = False if i < 3 else True
#         file_name = f"file{i}_hidden.md"
#         meta_files[file_name] = MetaFile(
#             path=Path(file_name),
#             abs_path=Path(f"docs/{file_name}"),
#             is_dir=is_dir,
#         )
