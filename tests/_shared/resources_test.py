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

import importlib.resources
import logging
from pathlib import Path
from typing import cast

import pytest
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.structure.files import Files
from pytest_check import check_functions as check

from mkdocs_publisher._extra.assets import stylesheets
from mkdocs_publisher._shared import resources

EXTRA_DIR = "mkdocs_publisher/_extra"
STYLESHEET_DIR = "assets/stylesheets"
STYLESHEET_FILE = "blog.min.css"
STYLESHEET_FILE_MAP = "blog.min.css.map"


def test_add_extra_existing_file(caplog: pytest.LogCaptureFixture) -> None:
    existing_file = Path(str(importlib.resources.files(stylesheets).joinpath(STYLESHEET_FILE)))
    expected_path = str(existing_file.relative_to(Path().cwd() / EXTRA_DIR))
    mkdocs_files = Files(files=[])
    mkdocs_config = cast(MkDocsConfig, MkDocsConfig())

    with caplog.at_level(level=logging.DEBUG):
        resources._add_extra_file(
            resource_file_path=existing_file,
            site_dir="",
            use_directory_urls=True,
            config_extra_files=mkdocs_config.extra_css,
            files=mkdocs_files,
        )

    check.equal(expected_path, mkdocs_files.css_files()[-1].src_uri)
    check.equal(expected_path, mkdocs_config.extra_css[-1])
    check.equal(caplog.records[-1].levelno, logging.DEBUG)
    check.is_in(expected_path, caplog.records[-1].message)


def test_add_extra_non_existing_file(caplog: pytest.LogCaptureFixture) -> None:
    existing_file = Path(str(importlib.resources.files(stylesheets).joinpath(f"{STYLESHEET_FILE}.non")))
    expected_path = str(existing_file.relative_to(Path().cwd() / EXTRA_DIR))
    mkdocs_files = Files(files=[])
    mkdocs_config = cast(MkDocsConfig, MkDocsConfig())

    with caplog.at_level(level=logging.DEBUG):
        resources._add_extra_file(
            resource_file_path=existing_file,
            site_dir="",
            use_directory_urls=True,
            config_extra_files=mkdocs_config.extra_css,
            files=mkdocs_files,
        )

    check.equal([], mkdocs_files.css_files())
    check.equal([], mkdocs_config.extra_css)
    check.equal(caplog.records[-1].levelno, logging.ERROR)
    check.is_in(expected_path, caplog.records[-1].message)


def test_add_stylesheet_file_with_map() -> None:
    mkdocs_files = Files(files=[])
    mkdocs_config = cast(MkDocsConfig, MkDocsConfig())
    expected_file_path = str(Path(STYLESHEET_DIR) / STYLESHEET_FILE)
    expected_file_map_path = str(Path(STYLESHEET_DIR) / STYLESHEET_FILE_MAP)

    resources.add_extra_css(
        stylesheet_file_name=STYLESHEET_FILE,
        config=mkdocs_config,
        files=mkdocs_files,
    )

    check.equal([expected_file_path, expected_file_map_path], list(mkdocs_files.src_paths.keys()))
    check.equal(expected_file_path, mkdocs_files.css_files()[-1].src_uri)
    check.equal([expected_file_path, expected_file_map_path], mkdocs_config.extra_css)


def test_add_stylesheet_file_without_map() -> None:
    mkdocs_files = Files(files=[])
    mkdocs_config = cast(MkDocsConfig, MkDocsConfig())
    expected_file_path = str(Path(STYLESHEET_DIR) / STYLESHEET_FILE)

    resources.add_extra_css(
        stylesheet_file_name=STYLESHEET_FILE,
        config=mkdocs_config,
        files=mkdocs_files,
        add_map=False,
    )

    check.equal([expected_file_path], list(mkdocs_files.src_paths.keys()))
    check.equal(expected_file_path, mkdocs_files.css_files()[-1].src_uri)
    check.equal([expected_file_path], mkdocs_config.extra_css)
