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
from typing import Optional
from typing import Union
from unittest.mock import patch

import pytest
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.structure.files import File
from mkdocs.structure.files import Files
from pytest import LogCaptureFixture
from pytest_check import check_functions as check

from mkdocs_publisher.meta.meta_files import MetaFile
from mkdocs_publisher.meta.meta_files import MetaFiles
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
def test_properties(path: Path, abs_path: Path, expected_name: str, expected_parent: str):
    meta_file = MetaFile(path=path, abs_path=abs_path, is_dir=False)

    check.equal(meta_file.name, expected_name, "Wrong name")
    check.equal(meta_file.parent, expected_parent, "Wrong parent")


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
def test_overview(
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

    check.is_(meta_file.is_overview, expected, "Wrong overview status")


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
def test_title(
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

    check.equal(meta_file.title, expected, "Wrong title")
    if warn is not None:
        check.equal(caplog.records[-1].levelno, logging.WARNING, "Wrong log level")
        check.equal(warn, caplog.records[-1].message, "Wrong log message")


@pytest.mark.parametrize(
    "pub_meta_plugin,meta,markdown,expected_publish,expected_redirect",
    [
        ({}, {"redirect": False}, "https://fake.com/", None, None),
        ({}, {"redirect": True}, "https://fake.com/", None, "https://fake.com/"),
        ({}, {"redirect": "https://fake.com/"}, "", None, "https://fake.com/"),
        ({}, {"redirect": False}, "fake_file.md", None, None),
        ({}, {"redirect": True}, "[Redirect](fake_file.md)", "hidden", "fake_file.md"),
        ({}, {"redirect": "fake_file.md"}, "", "hidden", "fake_file.md"),
        ({}, {"redirect": True}, "blah blah blah", None, None),
    ],
    indirect=["pub_meta_plugin"],
)
def test_redirect(
    mkdocs_config: MkDocsConfig,
    pub_meta_plugin: MetaPlugin,
    meta: dict,
    markdown: str,
    expected_publish: Optional[str],
    expected_redirect: Optional[str],
    caplog: LogCaptureFixture,
):
    meta_file: MetaFile = MetaFile(
        path=Path("fake_file.md"), abs_path=Path("/Users/me/docs/fake_file.md"), is_dir=False
    )
    meta_files: MetaFiles = MetaFiles()
    meta_files.set_configs(mkdocs_config=mkdocs_config, meta_plugin_config=pub_meta_plugin.config)
    new_meta = meta_files._get_redirect(meta_file=meta_file, meta=meta, markdown=markdown)

    if expected_publish:
        check.equal(new_meta["publish"], expected_publish, "Wrong publish")
    check.equal(meta_file.redirect, expected_redirect, "Wrong redirect")


def test_on_serve(mkdocs_config: MkDocsConfig, pub_meta_plugin: MetaPlugin):
    meta_files: MetaFiles = MetaFiles()
    meta_files.set_configs(mkdocs_config=mkdocs_config, meta_plugin_config=pub_meta_plugin.config)
    meta_files.on_serve = True

    check.is_true(meta_files.on_serve, "Wrong on serve status")


@pytest.mark.parametrize(
    "mkdocs_config,hidden_path,expected",
    [
        ({"docs_dir": "docs"}, None, []),
        ({"docs_dir": "docs"}, Path("docs/hidden_dir"), [Path("hidden_dir")]),
    ],
    indirect=["mkdocs_config"],
)
def test_add_hidden(
    mkdocs_config: MkDocsConfig,
    pub_meta_plugin: MetaPlugin,
    hidden_path: Optional[Path],
    expected: list,
):
    meta_files: MetaFiles = MetaFiles()
    meta_files.set_configs(mkdocs_config=mkdocs_config, meta_plugin_config=pub_meta_plugin.config)
    meta_files.add_hidden_path(hidden_path=hidden_path)

    check.equal(meta_files._hidden_paths, expected, "Wrong hidden paths")


def test_meta_file(
    mkdocs_config: MkDocsConfig,
    pub_meta_plugin: MetaPlugin,
):
    meta_files: MetaFiles = MetaFiles()
    meta_files.set_configs(mkdocs_config=mkdocs_config, meta_plugin_config=pub_meta_plugin.config)

    check.equal(meta_files.meta_file, "README.md", "Wrong meta file")


@pytest.mark.parametrize(
    "pub_meta_plugin,meta,on_serve,is_draft,is_hidden,warning",
    [
        ({}, {}, False, True, False, None),  # default file value is draft
        ({}, {"publish": True}, False, False, False, None),
        ({}, {"publish": "published"}, False, False, False, None),
        ({}, {"publish": False}, False, True, False, None),
        ({}, {"publish": "draft"}, False, True, False, None),
        ({}, {"publish": False}, True, False, False, None),  # when on_serve draft is published
        ({}, {"publish": "hidden"}, False, False, True, None),
        ({}, {"publish": "wrong"}, False, True, False, "Wrong key "),
        ({"publish": {"file_warn_on_missing": True}}, {}, False, True, False, "Missing "),
        ({"publish": {"file_warn_on_missing": False}}, {}, False, True, False, None),
    ],
    indirect=["pub_meta_plugin"],
)
def test_get_publish_status_for_files(
    caplog: LogCaptureFixture,
    mkdocs_config: MkDocsConfig,
    pub_meta_plugin: MetaPlugin,
    meta: dict,
    on_serve: bool,
    is_draft: bool,
    is_hidden: bool,
    warning: Optional[str],
):
    meta_files: MetaFiles = MetaFiles()
    meta_files.on_serve = on_serve
    meta_files.set_configs(mkdocs_config=mkdocs_config, meta_plugin_config=pub_meta_plugin.config)

    meta_file: MetaFile = MetaFile(
        path=Path("fake_file.md"), abs_path=Path("/Users/me/fake_file.md"), is_dir=False
    )
    meta_files._get_publish_status(meta_file=meta_file, meta=meta)

    check.equal(meta_file.is_draft, is_draft, "Wrong draft status")
    check.equal(meta_file.is_hidden, is_hidden, "Wrong hidden status")
    if warning is not None:
        check.equal(caplog.records[-1].levelno, logging.WARNING, "Wrong log level")
        check.is_true(caplog.records[-1].message.startswith(warning), "Wrong log message")


@pytest.mark.parametrize(
    "pub_meta_plugin,meta,on_serve,is_draft,is_hidden,warning",
    [
        ({}, {}, False, False, False, None),  # default dir value is published
        ({}, {"publish": True}, False, False, False, None),
        ({}, {"publish": "published"}, False, False, False, None),
        ({}, {"publish": False}, False, True, False, None),
        ({}, {"publish": "draft"}, False, True, False, None),
        ({}, {"publish": False}, True, False, False, None),  # when on_serve draft is published
        ({}, {"publish": "hidden"}, False, False, True, None),
        ({}, {"publish": "wrong"}, False, True, False, "Wrong key "),
        ({"publish": {"dir_warn_on_missing": True}}, {}, False, False, False, "Missing "),
        ({"publish": {"dir_warn_on_missing": False}}, {}, False, False, False, None),
    ],
    indirect=["pub_meta_plugin"],
)
def test_get_publish_status_for_dirs(
    caplog: LogCaptureFixture,
    mkdocs_config: MkDocsConfig,
    pub_meta_plugin: MetaPlugin,
    meta: dict,
    on_serve: bool,
    is_draft: bool,
    is_hidden: bool,
    warning: Optional[str],
):
    meta_files: MetaFiles = MetaFiles()
    meta_files.on_serve = on_serve
    meta_files.set_configs(mkdocs_config=mkdocs_config, meta_plugin_config=pub_meta_plugin.config)

    meta_file: MetaFile = MetaFile(path=Path("me"), abs_path=Path("/Users/me"), is_dir=True)
    meta_files._get_publish_status(meta_file=meta_file, meta=meta)

    check.equal(meta_file.is_draft, is_draft, "Wrong draft status")
    check.equal(meta_file.is_hidden, is_hidden, "Wrong hidden status")
    if warning is not None:
        check.equal(caplog.records[-1].levelno, logging.WARNING, "Wrong log level")
        check.is_true(caplog.records[-1].message.startswith(warning), "Wrong log message")


@pytest.mark.parametrize(
    "parent_meta,meta,is_draft,is_hidden",
    [
        ({"publish": False}, {"publish": True}, True, False),
        ({"publish": False}, {"publish": False}, True, False),
        ({"publish": False}, {"publish": "hidden"}, True, False),
        ({"publish": True}, {"publish": True}, False, False),
        ({"publish": True}, {"publish": False}, True, False),
        ({"publish": True}, {"publish": "hidden"}, False, True),
        ({"publish": "hidden"}, {"publish": True}, False, True),
        ({"publish": "hidden"}, {"publish": False}, False, True),
        ({"publish": "hidden"}, {"publish": "hidden"}, False, True),
    ],
)
def test_get_publish_status_with_parent(
    mkdocs_config: MkDocsConfig,
    pub_meta_plugin: MetaPlugin,
    parent_meta: dict,
    meta: dict,
    is_draft: bool,
    is_hidden: bool,
):
    meta_files: MetaFiles = MetaFiles()
    meta_files.set_configs(mkdocs_config=mkdocs_config, meta_plugin_config=pub_meta_plugin.config)

    meta_file_parent: MetaFile = MetaFile(path=Path("me"), abs_path=Path("/Users/me"), is_dir=True)
    meta_files["me"] = meta_file_parent
    meta_files._get_publish_status(meta_file=meta_file_parent, meta=parent_meta)

    meta_file: MetaFile = MetaFile(
        path=Path("me/fake_file.md"), abs_path=Path("/Users/me/fake_file.md"), is_dir=False
    )
    meta_files._get_publish_status(meta_file=meta_file, meta=meta)

    check.equal(meta_file.is_draft, is_draft)
    check.equal(meta_file.is_hidden, is_hidden)


@pytest.mark.parametrize(
    "publish_dir,publish_file,"
    "draft_all_keys,draft_file_keys,draft_dir_keys,"
    "hidden_all_keys,hidden_file_keys,hidden_dir_keys",
    [
        (
            False,
            False,
            {"me/fake_file.md", "me"},
            {"me/fake_file.md"},
            {"me"},
            set(),
            set(),
            set(),
        ),
        (False, True, {"me/fake_file.md", "me"}, {"me/fake_file.md"}, {"me"}, set(), set(), set()),
        (
            False,
            "hidden",
            {"me/fake_file.md", "me"},
            {"me/fake_file.md"},
            {"me"},
            set(),
            set(),
            set(),
        ),
        (True, False, {"me/fake_file.md"}, {"me/fake_file.md"}, set(), set(), set(), set()),
        (True, True, set(), set(), set(), set(), set(), set()),
        (True, "hidden", set(), set(), set(), {"me/fake_file.md"}, {"me/fake_file.md"}, set()),
        (
            "hidden",
            False,
            set(),
            set(),
            set(),
            {"me/fake_file.md", "me"},
            {"me/fake_file.md"},
            {"me"},
        ),
        (
            "hidden",
            True,
            set(),
            set(),
            set(),
            {"me/fake_file.md", "me"},
            {"me/fake_file.md"},
            {"me"},
        ),
        (
            "hidden",
            "hidden",
            set(),
            set(),
            set(),
            {"me/fake_file.md", "me"},
            {"me/fake_file.md"},
            {"me"},
        ),
    ],
)
def test_drafts_and_hidden(
    mkdocs_config: MkDocsConfig,
    pub_meta_plugin: MetaPlugin,
    patched_meta_files: MetaFiles,
    publish_dir: Union[str, bool],
    publish_file: Union[str, bool],
    draft_all_keys: list[str],
    draft_file_keys: list[str],
    draft_dir_keys: list[str],
    hidden_all_keys: list[str],
    hidden_file_keys: list[str],
    hidden_dir_keys: list[str],
):
    patched_meta_files.set_configs(
        mkdocs_config=mkdocs_config, meta_plugin_config=pub_meta_plugin.config
    )

    meta_file_dir: MetaFile = MetaFile(path=Path("me"), abs_path=Path("/Users/me"), is_dir=True)
    patched_meta_files["me"] = meta_file_dir
    patched_meta_files._get_publish_status(meta_file=meta_file_dir, meta={"publish": publish_dir})

    meta_file: MetaFile = MetaFile(
        path=Path("me/fake_file.md"), abs_path=Path("/Users/me/fake_file.md"), is_dir=False
    )
    patched_meta_files["me/fake_file.md"] = meta_file
    patched_meta_files._get_publish_status(meta_file=meta_file, meta={"publish": publish_file})

    check.equal(set(patched_meta_files.drafts().keys()), draft_all_keys)
    check.equal(set(patched_meta_files.drafts(files=True).keys()), draft_file_keys)
    check.equal(set(patched_meta_files.drafts(dirs=True).keys()), draft_dir_keys)
    check.equal(set(patched_meta_files.hidden().keys()), hidden_all_keys)
    check.equal(set(patched_meta_files.hidden(files=True).keys()), hidden_file_keys)
    check.equal(set(patched_meta_files.hidden(dirs=True).keys()), hidden_dir_keys)


@pytest.mark.parametrize("exists", [True, False])
def test_add_dir(
    mkdocs_config: MkDocsConfig, pub_meta_plugin: MetaPlugin, exists, patched_meta_files: MetaFiles
):
    patched_meta_files.set_configs(
        mkdocs_config=mkdocs_config, meta_plugin_config=pub_meta_plugin.config
    )

    meta_file_dir: MetaFile = MetaFile(path=Path("me"), abs_path=Path("/Users/me"), is_dir=True)
    with patch.object(Path, "exists", return_value=exists):
        patched_meta_files["me"] = meta_file_dir
        patched_meta_files._get_publish_status(meta_file=meta_file_dir, meta={})

    check.is_true("me" in patched_meta_files)


@pytest.mark.parametrize(
    "path,is_dir,ignored_dirs,expected",
    [
        ("tests/_tests_data/fake_file.md", False, [], ["fake_file.md"]),
        ("tests/_tests_data/fake_dir", True, [], ["fake_dir"]),
        ("tests/_tests_data/fake_dir", True, ["tests/_tests_data/fake_dir"], []),
        ("tests/_tests_data/no_md.pic", False, ["fake_dir"], []),
    ],
)
def test_add_meta_files(
    mkdocs_config: MkDocsConfig,
    pub_meta_plugin: MetaPlugin,
    patched_meta_files: MetaFiles,
    path: str,
    is_dir: bool,
    ignored_dirs: list[str],
    expected: list[str],
):
    patched_meta_files.set_configs(
        mkdocs_config=mkdocs_config, meta_plugin_config=pub_meta_plugin.config
    )
    with (
        patch.object(Path, "is_dir", return_value=is_dir),
        patch.object(Path, "rglob", return_value=[Path(path)]),
    ):
        patched_meta_files.add_meta_files(
            ignored_dirs=[Path(ignored_dir) for ignored_dir in ignored_dirs]
        )

    check.equal(list(patched_meta_files.keys()), expected)


def test_files_gen(
    mkdocs_config: MkDocsConfig,
    pub_meta_plugin: MetaPlugin,
    patched_meta_files: MetaFiles,
):
    patched_meta_files.set_configs(
        mkdocs_config=mkdocs_config, meta_plugin_config=pub_meta_plugin.config
    )
    files_paths: list[str] = ["tests/_tests_data/fake_data.md", "tests/_tests_data/fake_file.md"]
    for path in files_paths:
        with (
            patch.object(Path, "is_dir", return_value=False),
            patch.object(Path, "rglob", return_value=[Path(path)]),
        ):
            patched_meta_files.add_meta_files(ignored_dirs=[])

    gen_files_paths = []
    for file in patched_meta_files.files_gen():
        gen_files_paths.append(str(file.abs_path))

    check.equal(files_paths, gen_files_paths)


@pytest.mark.parametrize(
    "redirect,expected_nr_of_files",
    [
        ("https://fake.url/", 0),
        ("fake.md", 1),
        (None, 1),
    ],
)
def test_clean_redirect_files(
    mkdocs_config: MkDocsConfig,
    pub_meta_plugin: MetaPlugin,
    patched_meta_files: MetaFiles,
    redirect: Optional[str],
    expected_nr_of_files: int,
):
    patched_meta_files.set_configs(
        mkdocs_config=mkdocs_config, meta_plugin_config=pub_meta_plugin.config
    )
    meta_file: MetaFile = MetaFile(
        path=Path("fake_url_redirect.md"),
        abs_path=Path("/Users/me/fake_url_redirect.md"),
        is_dir=False,
    )

    patched_meta_files["fake_url_redirect.md"] = meta_file
    patched_meta_files["fake_url_redirect.md"].redirect = redirect

    files = Files(
        files=[
            File(
                path="fake_url_redirect.md",
                src_dir="/Users/me/",
                dest_dir="/Users/docs",
                use_directory_urls=True,
            )
        ]
    )

    new_files = patched_meta_files.clean_redirect_files(files=files)
    check.equal(redirect, patched_meta_files["fake_url_redirect.md"].redirect)
    check.equal(expected_nr_of_files, len(new_files))


@pytest.mark.parametrize(
    "redirect,expected_result",
    [
        ("https://fake.url/", None),
        ("fake_url_redirect.md", "<!--"),
        (None, None),
    ],
)
def test_generate_redirect_page(
    mkdocs_config: MkDocsConfig,
    pub_meta_plugin: MetaPlugin,
    patched_meta_files: MetaFiles,
    redirect: Optional[str],
    expected_result: Optional[str],
):
    patched_meta_files.set_configs(
        mkdocs_config=mkdocs_config, meta_plugin_config=pub_meta_plugin.config
    )

    meta_file: MetaFile = MetaFile(
        path=Path("fake_url_redirect.md"),
        abs_path=Path("/Users/me/fake_url_redirect.md"),
        is_dir=False,
    )

    patched_meta_files["fake_url_redirect.md"] = meta_file
    patched_meta_files["fake_url_redirect.md"].redirect = redirect
    patched_meta_files["fake_url_redirect.md"].url = redirect

    file = File(
        path="fake_url_redirect.md",
        src_dir="/Users/me/",
        dest_dir="/Users/docs",
        use_directory_urls=True,
    )

    generated_file = patched_meta_files.generate_redirect_page(file=file)
    if expected_result is None:
        check.equal(expected_result, generated_file)
    else:
        check.is_in(expected_result, generated_file)


@pytest.mark.parametrize(
    "mkdocs_config,pub_meta_plugin,path,with_meta_file,file_slug,dir_slug,ignored_dir,expected_url",
    [
        ({"docs_dir": "me"}, {}, "fake_file.md", True, None, None, None, "fake-file/"),
        ({"docs_dir": "me"}, {}, "fake_file.md", True, "file-slug", None, None, "file-slug/"),
        ({"docs_dir": "me"}, {}, "fake_file.md", False, None, None, None, "fake_file/"),
        ({"docs_dir": "me"}, {}, "fake_file.jpeg", False, None, None, None, "fake_file.jpeg"),
        ({"docs_dir": "me"}, {}, "me/fake_file.md", True, None, None, None, "me/fake-file/"),
        (
            {"docs_dir": "me"},
            {},
            "me/fake_file.md",
            True,
            "file-slug",
            None,
            None,
            "me/file-slug/",
        ),
        ({"docs_dir": "me"}, {}, "me/fake_file.md", False, None, None, None, "me/fake_file/"),
        (
            {"docs_dir": "me"},
            {},
            "me/fake_file.jpeg",
            False,
            None,
            None,
            None,
            "me/fake_file.jpeg",
        ),
        (
            {"docs_dir": "me"},
            {},
            "me/fake_file.md",
            True,
            None,
            "dir-slug",
            None,
            "dir-slug/fake-file/",
        ),
        (
            {"docs_dir": "me"},
            {},
            "me/fake_file.md",
            True,
            "file-slug",
            "dir-slug",
            None,
            "dir-slug/file-slug/",
        ),
        (
            {"docs_dir": "me"},
            {},
            "me/fake_file.md",
            False,
            None,
            "dir-slug",
            None,
            "dir-slug/fake_file/",
        ),
        (
            {"docs_dir": "me"},
            {},
            "me/fake_file.jpeg",
            False,
            None,
            "dir-slug",
            None,
            "dir-slug/fake_file.jpeg",
        ),
        ({"docs_dir": "me"}, {}, "fake_file.md", True, None, None, "/Users/me", "fake-file/"),
        ({"docs_dir": "me"}, {}, "me/fake_file.md", True, None, None, "/Users/me", None),
        (
            {"docs_dir": "me"},
            {"slug": {"enabled": False}},
            "fake_file.md",
            True,
            None,
            None,
            None,
            "fake_file/",
        ),
        ({"docs_dir": "me"}, {}, ".", False, None, None, None, "."),
    ],
    indirect=["mkdocs_config", "pub_meta_plugin"],
)
def test_change_files_slug(
    mkdocs_config: MkDocsConfig,
    pub_meta_plugin: MetaPlugin,
    patched_meta_files: MetaFiles,
    path: str,
    with_meta_file: bool,
    file_slug: Optional[str],
    dir_slug: Optional[str],
    ignored_dir: Optional[str],
    expected_url: Optional[str],
):
    patched_meta_files.set_configs(
        mkdocs_config=mkdocs_config, meta_plugin_config=pub_meta_plugin.config
    )

    meta_dir: MetaFile = MetaFile(
        path=Path("me"),
        abs_path=Path("/Users/me/README.md"),
        is_dir=True,
    )
    with patch.object(Path, "exists", return_value=True):
        patched_meta_files["me"] = meta_dir
    if dir_slug:
        meta_dir.slug = dir_slug

    if with_meta_file:
        meta_file: MetaFile = MetaFile(
            path=Path(path),
            abs_path=Path(f"/Users/me/{'index.md' if path == '.' else path}"),
            is_dir=False,
        )
        with patch.object(Path, "exists", return_value=True):
            patched_meta_files[path] = meta_file
        meta_file.is_draft = False
        if file_slug:
            meta_file.slug = file_slug

    files = Files(
        [
            File(
                path=path,
                src_dir="/Users",
                dest_dir="/Users/out",
                use_directory_urls=True,
            )
        ]
    )
    new_files = patched_meta_files.change_files_slug(
        files=files, ignored_dirs=[Path(ignored_dir)] if ignored_dir else []
    )
    new_file = new_files.get_file_from_path(path)
    if expected_url:
        check.equal(expected_url, new_file.url)
    else:
        check.is_none(new_file)
