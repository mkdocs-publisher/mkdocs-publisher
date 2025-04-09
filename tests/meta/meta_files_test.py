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
from pathlib import Path
from unittest.mock import patch

import pytest
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.structure.files import File
from mkdocs.structure.files import Files
from pytest_check import check_functions as check

from mkdocs_publisher.meta.meta_files import MetaFile
from mkdocs_publisher.meta.meta_files import MetaFiles
from mkdocs_publisher.meta.plugin import MetaPlugin


@pytest.mark.parametrize(
    ("path", "abs_path", "expected_name", "expected_parent"),
    [
        (Path("docs/fake_file.md"), Path("/Users/docs/fake_file.md"), "fake_file.md", Path("docs")),
        (Path("fake_file.md"), Path("/Users/docs/fake_file.md"), "fake_file.md", None),
    ],
)
def test_properties(path: Path, abs_path: Path, expected_name: str, expected_parent: str) -> None:
    meta_file = MetaFile(path=path, abs_path=abs_path, is_dir=False)

    check.equal(meta_file.name, expected_name, "Wrong name")
    check.equal(meta_file.parent, expected_parent, "Wrong parent")


@pytest.mark.parametrize(
    ("pub_meta_plugin", "meta", "markdown", "is_dir", "expected"),
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
) -> None:
    meta_file: MetaFile = MetaFile(path=Path("fake_file.md"), abs_path=Path("/Users/docs/fake_file.md"), is_dir=is_dir)

    meta_files: MetaFiles = MetaFiles()
    meta_files.set_configs(mkdocs_config=mkdocs_config, meta_plugin_config=pub_meta_plugin.config)
    meta_files._get_overview(meta_file=meta_file, meta=meta, markdown=markdown)

    check.is_(meta_file.is_overview, expected, "Wrong overview status")


@pytest.mark.parametrize(
    ("pub_meta_plugin", "meta", "markdown", "is_dir", "expected", "warn"),
    [
        ({}, {"title": "Some title"}, "", False, "Some title", None),
        ({}, {"title": "Some title"}, "", True, "Some title", None),
        ({}, {}, "# Title", False, "Title", 'Title value from "title" meta data is missing for file: "fake_file.md"'),
        ({}, {}, "", False, "Fake File", 'Title value from first heading is missing for file: "fake_file.md"'),
        ({"title": {"warn_on_missing_meta": False}}, {}, "# Title", False, "Title", None),
        ({"title": {"warn_on_missing_header": False}}, {}, "", False, "Fake File", None),
        ({"title": {"mode": "head"}}, {}, "# Title", False, "Title", None),
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
    warn: str | None,
    caplog: pytest.LogCaptureFixture,
) -> None:
    meta_file: MetaFile = MetaFile(path=Path("fake_file.md"), abs_path=Path("/Users/docs/fake_file.md"), is_dir=is_dir)

    meta_files: MetaFiles = MetaFiles()
    meta_files.set_configs(mkdocs_config=mkdocs_config, meta_plugin_config=pub_meta_plugin.config)
    meta_files._get_title(meta_file=meta_file, meta=meta, markdown=markdown)

    check.equal(meta_file.title, expected, "Wrong title")
    if warn is not None:
        check.equal(caplog.records[-1].levelno, logging.WARNING, "Wrong log level")
        check.equal(warn, caplog.records[-1].message, "Wrong log message")


@pytest.mark.parametrize(
    ("meta", "markdown", "expected_publish", "expected_redirect"),
    [
        ({"redirect": False}, "https://fake.com/", None, None),
        ({"redirect": True}, "https://fake.com/", None, "https://fake.com/"),
        ({"redirect": "https://fake.com/"}, "", None, "https://fake.com/"),
        ({"redirect": False}, "fake_file.md", None, None),
        ({"redirect": True}, "[Redirect](fake_file.md)", "hidden", "fake_file.md"),
        ({"redirect": "fake_file.md"}, "", "hidden", "fake_file.md"),
        ({"redirect": True}, "blah blah blah", None, None),
    ],
)
def test_redirect(
    mkdocs_config: MkDocsConfig,
    pub_meta_plugin: MetaPlugin,
    meta: dict,
    markdown: str,
    expected_publish: str | None,
    expected_redirect: str | None,
) -> None:
    meta_file: MetaFile = MetaFile(path=Path("fake_file.md"), abs_path=Path("/Users/docs/fake_file.md"), is_dir=False)

    meta_files: MetaFiles = MetaFiles()
    meta_files.set_configs(mkdocs_config=mkdocs_config, meta_plugin_config=pub_meta_plugin.config)
    new_meta = meta_files._get_redirect(meta_file=meta_file, meta=meta, markdown=markdown)

    if expected_publish:
        check.equal(new_meta["publish"], expected_publish, "Wrong publish")
    check.equal(meta_file.redirect, expected_redirect, "Wrong redirect")


def test_on_serve(mkdocs_config: MkDocsConfig, pub_meta_plugin: MetaPlugin) -> None:
    meta_files: MetaFiles = MetaFiles()
    meta_files.set_configs(mkdocs_config=mkdocs_config, meta_plugin_config=pub_meta_plugin.config)
    meta_files.on_serve = True

    check.is_true(meta_files.on_serve, "Wrong on serve status")


@pytest.mark.parametrize(
    ("hidden_path", "expected"),
    [
        (None, []),
        (Path("docs/hidden_dir"), [Path("hidden_dir")]),
    ],
)
def test_add_hidden(
    mkdocs_config: MkDocsConfig,
    pub_meta_plugin: MetaPlugin,
    hidden_path: Path | None,
    expected: list,
) -> None:
    meta_files: MetaFiles = MetaFiles()
    meta_files.set_configs(mkdocs_config=mkdocs_config, meta_plugin_config=pub_meta_plugin.config)
    meta_files.add_hidden_path(hidden_path=hidden_path)

    check.equal(meta_files._hidden_paths, expected, "Wrong hidden paths")


def test_meta_file(
    mkdocs_config: MkDocsConfig,
    pub_meta_plugin: MetaPlugin,
) -> None:
    meta_files: MetaFiles = MetaFiles()
    meta_files.set_configs(mkdocs_config=mkdocs_config, meta_plugin_config=pub_meta_plugin.config)

    check.equal(meta_files.dir_meta_file, "README.md", "Wrong meta file")


@pytest.mark.parametrize(
    ("pub_meta_plugin", "meta", "on_serve", "is_draft", "is_hidden", "warning"),
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
    caplog: pytest.LogCaptureFixture,
    mkdocs_config: MkDocsConfig,
    pub_meta_plugin: MetaPlugin,
    meta: dict,
    on_serve: bool,
    is_draft: bool,
    is_hidden: bool,
    warning: str | None,
) -> None:
    meta_files: MetaFiles = MetaFiles()
    meta_files.on_serve = on_serve
    meta_files.set_configs(mkdocs_config=mkdocs_config, meta_plugin_config=pub_meta_plugin.config)

    meta_file: MetaFile = MetaFile(path=Path("fake_file.md"), abs_path=Path("/Users/docs/fake_file.md"), is_dir=False)
    meta_files._get_publish_status(meta_file=meta_file, meta=meta)

    check.equal(meta_file.is_draft, is_draft, "Wrong draft status")
    check.equal(meta_file.is_hidden, is_hidden, "Wrong hidden status")
    if warning is not None:
        check.equal(caplog.records[-1].levelno, logging.WARNING, "Wrong log level")
        check.is_true(caplog.records[-1].message.startswith(warning), "Wrong log message")


@pytest.mark.parametrize(
    ("pub_meta_plugin", "meta", "on_serve", "is_draft", "is_hidden", "warning"),
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
    caplog: pytest.LogCaptureFixture,
    mkdocs_config: MkDocsConfig,
    pub_meta_plugin: MetaPlugin,
    meta: dict,
    on_serve: bool,
    is_draft: bool,
    is_hidden: bool,
    warning: str | None,
) -> None:
    meta_files: MetaFiles = MetaFiles()
    meta_files.on_serve = on_serve
    meta_files.set_configs(mkdocs_config=mkdocs_config, meta_plugin_config=pub_meta_plugin.config)

    meta_file: MetaFile = MetaFile(path=Path("me"), abs_path=Path("/Users/docs/me"), is_dir=True)
    meta_files._get_publish_status(meta_file=meta_file, meta=meta)

    check.equal(meta_file.is_draft, is_draft, "Wrong draft status")
    check.equal(meta_file.is_hidden, is_hidden, "Wrong hidden status")
    if warning is not None:
        check.equal(caplog.records[-1].levelno, logging.WARNING, "Wrong log level")
        check.is_true(caplog.records[-1].message.startswith(warning), "Wrong log message")


@pytest.mark.parametrize(
    ("parent_meta", "meta", "is_draft", "is_hidden"),
    [
        ({"publish": False}, {"publish": True}, True, False),
        ({"publish": False}, {"publish": False}, True, False),
        ({"publish": False}, {"publish": "hidden"}, True, False),
        ({"publish": True}, {"publish": True}, False, False),
        ({"publish": True}, {"publish": False}, True, False),
        ({"publish": True}, {"publish": "hidden"}, False, True),
        ({"publish": "hidden"}, {"publish": True}, False, True),
        ({"publish": "hidden"}, {"publish": False}, True, False),
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
) -> None:
    meta_files: MetaFiles = MetaFiles()
    meta_files.set_configs(mkdocs_config=mkdocs_config, meta_plugin_config=pub_meta_plugin.config)

    meta_file_parent: MetaFile = MetaFile(path=Path("docs"), abs_path=Path("/Users/docs"), is_dir=True)
    meta_files["docs"] = meta_file_parent
    meta_files._get_publish_status(meta_file=meta_file_parent, meta=parent_meta)

    meta_file: MetaFile = MetaFile(
        path=Path("docs/fake_file.md"),
        abs_path=Path("/Users/docs/fake_file.md"),
        is_dir=False,
    )
    meta_files._get_publish_status(meta_file=meta_file, meta=meta)

    check.equal(meta_file.is_draft, is_draft)
    check.equal(meta_file.is_hidden, is_hidden)


@pytest.mark.parametrize(
    (
        "publish_dir",
        "publish_file",
        "is_overview",
        "drafts_keys",
        "draft_file_keys",
        "draft_dir_keys",
        "hidden_keys",
        "hidden_file_keys",
        "hidden_dir_keys",
    ),
    [
        (False, False, False, {"docs/fake_file.md", "docs"}, {"docs/fake_file.md"}, {"docs"}, set(), set(), set()),
        (False, True, False, {"docs/fake_file.md", "docs"}, {"docs/fake_file.md"}, {"docs"}, set(), set(), set()),
        (False, "hidden", False, {"docs/fake_file.md", "docs"}, {"docs/fake_file.md"}, {"docs"}, set(), set(), set()),
        (True, False, False, {"docs/fake_file.md"}, {"docs/fake_file.md"}, set(), set(), set(), set()),
        (True, True, False, set(), set(), set(), set(), set(), set()),
        (True, "hidden", False, set(), set(), set(), {"docs/fake_file.md"}, {"docs/fake_file.md"}, set()),
        ("hidden", False, False, {"docs/fake_file.md"}, {"docs/fake_file.md"}, set(), {"docs"}, set(), {"docs"}),
        ("hidden", True, False, set(), set(), set(), {"docs/fake_file.md", "docs"}, {"docs/fake_file.md"}, {"docs"}),
        (
            "hidden",
            "hidden",
            False,
            set(),
            set(),
            set(),
            {"docs/fake_file.md", "docs"},
            {"docs/fake_file.md"},
            {"docs"},
        ),
        (
            False,
            False,
            True,
            {"docs/fake_file.md", "docs"},
            {"docs/fake_file.md", "docs/README.md"},
            {"docs"},
            set(),
            set(),
            set(),
        ),
        (
            False,
            True,
            True,
            {"docs/fake_file.md", "docs"},
            {"docs/fake_file.md", "docs/README.md"},
            {"docs"},
            set(),
            set(),
            set(),
        ),
        (
            False,
            "hidden",
            True,
            {"docs/fake_file.md", "docs"},
            {"docs/fake_file.md", "docs/README.md"},
            {"docs"},
            set(),
            set(),
            set(),
        ),
        (True, False, True, {"docs/fake_file.md"}, {"docs/fake_file.md"}, set(), set(), set(), set()),
        (True, True, True, set(), set(), set(), set(), set(), set()),
        (True, "hidden", True, set(), set(), set(), {"docs/fake_file.md"}, {"docs/fake_file.md"}, set()),
        (
            "hidden",
            False,
            True,
            {"docs/fake_file.md"},
            {"docs/fake_file.md"},
            set(),
            {"docs"},
            {"docs/README.md"},
            {"docs"},
        ),
        (
            "hidden",
            True,
            True,
            set(),
            set(),
            set(),
            {"docs/fake_file.md", "docs"},
            {"docs/fake_file.md", "docs/README.md"},
            {"docs"},
        ),
        (
            "hidden",
            "hidden",
            True,
            set(),
            set(),
            set(),
            {"docs/fake_file.md", "docs"},
            {"docs/fake_file.md", "docs/README.md"},
            {"docs"},
        ),
    ],
)
def test_drafts_and_hidden(
    mkdocs_config: MkDocsConfig,
    pub_meta_plugin: MetaPlugin,
    is_overview: bool,
    patched_meta_files: MetaFiles,
    publish_dir: str | bool,
    publish_file: str | bool,
    drafts_keys: list[str],
    draft_file_keys: list[str],
    draft_dir_keys: list[str],
    hidden_keys: list[str],
    hidden_file_keys: list[str],
    hidden_dir_keys: list[str],
) -> None:
    patched_meta_files.set_configs(mkdocs_config=mkdocs_config, meta_plugin_config=pub_meta_plugin.config)

    meta_file_dir: MetaFile = MetaFile(
        path=Path("docs"),
        abs_path=Path("/Users/docs"),
        is_dir=True,
        is_overview=is_overview,
    )
    patched_meta_files["docs"] = meta_file_dir
    patched_meta_files._get_publish_status(meta_file=meta_file_dir, meta={"publish": publish_dir})

    meta_file: MetaFile = MetaFile(
        path=Path("docs/fake_file.md"),
        abs_path=Path("/Users/docs/fake_file.md"),
        is_dir=False,
    )
    patched_meta_files["docs/fake_file.md"] = meta_file
    patched_meta_files._get_publish_status(meta_file=meta_file, meta={"publish": publish_file})

    check.equal(set(patched_meta_files.drafts.keys()), drafts_keys, "Wrong drafts keys")
    check.equal(set(patched_meta_files.draft_files.keys()), draft_file_keys, "Wrong draft files keys")
    check.equal(set(patched_meta_files.draft_dirs.keys()), draft_dir_keys, "Wrong draft dirs keys")
    check.equal(set(patched_meta_files.hidden.keys()), hidden_keys, "Wrong hidden keys")
    check.equal(set(patched_meta_files.hidden_files.keys()), hidden_file_keys, "Wrong hidden files keys")
    check.equal(set(patched_meta_files.hidden_dirs.keys()), hidden_dir_keys, "Wrong hidden dirs keys")


@pytest.mark.parametrize(("is_draft", "expected_files"), [(False, 1), (True, 0)])
def test_clean_draft_files(
    mkdocs_config: MkDocsConfig,
    pub_meta_plugin: MetaPlugin,
    patched_meta_files: MetaFiles,
    caplog: pytest.LogCaptureFixture,
    is_draft: bool,
    expected_files: int,
) -> None:
    patched_meta_files.set_configs(mkdocs_config=mkdocs_config, meta_plugin_config=pub_meta_plugin.config)
    meta_file: MetaFile = MetaFile(path=Path("fake_file.md"), abs_path=Path("/docs/fake_file.md"), is_dir=False)
    patched_meta_files["fake_file.md"] = meta_file
    patched_meta_files["fake_file.md"].is_draft = is_draft

    files = Files(
        files=[
            File(
                path="fake_file.md",
                src_dir="docs/",
                dest_dir="site/",
                use_directory_urls=True,
            ),
        ],
    )

    new_files = patched_meta_files.clean_draft_files(files=files)

    check.equal(len(new_files), expected_files, "Wrong number of files")
    if expected_files == 0:
        check.equal(caplog.records[-1].levelno, logging.DEBUG, "Wrong log level")
        check.is_true(caplog.records[-1].message.startswith("Removed draft file:"), "Wrong log message")
    elif expected_files == 1:
        check.equal(next(iter(new_files.src_paths.keys())), "fake_file.md")


@pytest.mark.parametrize("exists", [True, False])
def test_add_dir(
    mkdocs_config: MkDocsConfig,
    pub_meta_plugin: MetaPlugin,
    exists: bool,
    patched_meta_files: MetaFiles,
) -> None:
    patched_meta_files.set_configs(mkdocs_config=mkdocs_config, meta_plugin_config=pub_meta_plugin.config)

    meta_file_dir: MetaFile = MetaFile(path=Path("docs"), abs_path=Path("/Users/docs"), is_dir=True)
    with patch.object(Path, "exists", return_value=exists):
        patched_meta_files["docs"] = meta_file_dir
        patched_meta_files._get_publish_status(meta_file=meta_file_dir, meta={})

    check.is_true("docs" in patched_meta_files)


@pytest.mark.parametrize(
    ("path", "is_dir", "ignored_dirs", "expected"),
    [
        ("docs/fake_file.md", False, [], ["fake_file.md"]),
        ("docs/fake_dir", True, [], ["fake_dir"]),
        ("docs/fake_dir", True, ["docs/fake_dir"], []),
        ("docs/no_md.pic", False, ["fake_dir"], []),
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
) -> None:
    patched_meta_files.set_configs(mkdocs_config=mkdocs_config, meta_plugin_config=pub_meta_plugin.config)
    with (
        patch.object(Path, "is_dir", return_value=is_dir),
        patch.object(Path, "rglob", return_value=[Path(path)]),
    ):
        patched_meta_files.add_files(ignored_dirs=[Path(ignored_dir) for ignored_dir in ignored_dirs])

    check.equal(list(patched_meta_files.keys()), expected)


def test_files_generator(
    mkdocs_config: MkDocsConfig,
    pub_meta_plugin: MetaPlugin,
    patched_meta_files: MetaFiles,
) -> None:
    patched_meta_files.set_configs(mkdocs_config=mkdocs_config, meta_plugin_config=pub_meta_plugin.config)
    files_paths: list[str] = ["docs/fake_data.md", "docs/fake_file.md"]
    for path in files_paths:
        with (
            patch.object(Path, "is_dir", return_value=False),
            patch.object(Path, "rglob", return_value=[Path(path)]),
        ):
            patched_meta_files.add_files(ignored_dirs=[])

    gen_files_paths = [str(file.abs_path) for file in patched_meta_files.generator()]

    check.equal(files_paths, gen_files_paths)


@pytest.mark.parametrize(
    ("redirect", "expected_nr_of_files"),
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
    redirect: str | None,
    expected_nr_of_files: int,
) -> None:
    patched_meta_files.set_configs(mkdocs_config=mkdocs_config, meta_plugin_config=pub_meta_plugin.config)
    meta_file: MetaFile = MetaFile(
        path=Path("fake_url_redirect.md"),
        abs_path=Path("docs/fake_url_redirect.md"),
        is_dir=False,
    )

    patched_meta_files["fake_url_redirect.md"] = meta_file
    patched_meta_files["fake_url_redirect.md"].redirect = redirect

    files = Files(
        files=[
            File(
                path="fake_url_redirect.md",
                src_dir="docs/",
                dest_dir="site",
                use_directory_urls=True,
            ),
        ],
    )

    new_files = patched_meta_files.clean_redirect_files(files=files)
    check.equal(redirect, patched_meta_files["fake_url_redirect.md"].redirect)
    check.equal(expected_nr_of_files, len(new_files))


@pytest.mark.parametrize(
    ("redirect", "expected_result"),
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
    redirect: str | None,
    expected_result: str | None,
) -> None:
    patched_meta_files.set_configs(mkdocs_config=mkdocs_config, meta_plugin_config=pub_meta_plugin.config)

    meta_file: MetaFile = MetaFile(
        path=Path("fake_url_redirect.md"),
        abs_path=Path("docs/fake_url_redirect.md"),
        is_dir=False,
    )

    patched_meta_files["fake_url_redirect.md"] = meta_file
    patched_meta_files["fake_url_redirect.md"].redirect = redirect
    patched_meta_files["fake_url_redirect.md"].url = redirect

    file = File(
        path="fake_url_redirect.md",
        src_dir="docs/",
        dest_dir="site/",
        use_directory_urls=True,
    )

    generated_file = patched_meta_files.generate_redirect_page(file=file)
    if expected_result is None:
        check.equal(expected_result, generated_file)
    else:
        check.is_in(expected_result, generated_file)  # type: ignore[reportArgumentType]


@pytest.mark.parametrize(
    ("path", "with_meta_file", "file_slug", "dir_slug", "expected_url"),
    [
        ("fake_file.md", True, None, None, "fake-file/"),
        ("fake_file.md", True, "file-slug", None, "file-slug/"),
        ("fake_file.md", False, None, None, "fake_file/"),
        ("fake_file.jpeg", False, None, None, "fake_file.jpeg"),
        ("docs/fake_file.md", True, None, None, "docs/fake-file/"),
        ("docs/fake_file.md", True, "file-slug", None, "docs/file-slug/"),
        ("docs/fake_file.md", False, None, None, "docs/fake_file/"),
        ("docs/fake_file.jpeg", False, None, None, "docs/fake_file.jpeg"),
        ("docs/fake_file.md", True, None, "dir-slug", "dir-slug/fake-file/"),
        ("docs/fake_file.md", True, "file-slug", "dir-slug", "dir-slug/file-slug/"),
        ("docs/fake_file.md", False, None, "dir-slug", "dir-slug/fake_file/"),
        ("docs/fake_file.jpeg", False, None, "dir-slug", "dir-slug/fake_file.jpeg"),
        (".", False, None, None, "."),
    ],
)
def test_change_file_slug(
    mkdocs_config: MkDocsConfig,
    pub_meta_plugin: MetaPlugin,
    patched_meta_files: MetaFiles,
    path: str,
    with_meta_file: bool,
    file_slug: str | None,
    dir_slug: str | None,
    expected_url: str | None,
) -> None:
    patched_meta_files.set_configs(mkdocs_config=mkdocs_config, meta_plugin_config=pub_meta_plugin.config)

    meta_dir: MetaFile = MetaFile(
        path=Path("docs"),
        abs_path=Path("/Users/docs/README.md"),
        is_dir=True,
    )
    with patch.object(Path, "exists", return_value=True):
        patched_meta_files["docs"] = meta_dir
    if dir_slug:
        meta_dir.slug = dir_slug

    if with_meta_file:
        meta_file: MetaFile = MetaFile(
            path=Path(path),
            abs_path=Path(f"/Users/docs/{'index.md' if path == '.' else path}"),
            is_dir=False,
        )
        with patch.object(Path, "exists", return_value=True):
            patched_meta_files[path] = meta_file
        if file_slug:
            meta_file.slug = file_slug

    file = File(
        path=path,
        src_dir="/Users/docs",
        dest_dir="/Users/site",
        use_directory_urls=True,
    )

    patched_meta_files._change_file_slug(file=file, file_path=Path(path))

    check.equal(expected_url, file.url)


@pytest.mark.parametrize(
    ("pub_meta_plugin", "path", "with_meta_file", "is_draft", "ignored_dir", "expected_url"),
    [
        ({}, "fake_file.md", True, False, "/Users/me", "fake-file/"),
        ({}, "fake_file.md", False, False, None, "fake_file/"),
        ({}, "fake_file.md", True, True, None, None),
        ({}, "docs/fake_file.md", True, False, "/Users/docs", None),
        ({"slug": {"enabled": False}}, "fake_file.md", True, False, None, "fake_file/"),
    ],
    indirect=["pub_meta_plugin"],
)
def test_change_files_slug(
    mkdocs_config: MkDocsConfig,
    pub_meta_plugin: MetaPlugin,
    patched_meta_files: MetaFiles,
    path: str,
    with_meta_file: bool,
    is_draft: bool,
    ignored_dir: str | None,
    expected_url: str | None,
) -> None:
    patched_meta_files = MetaFiles()
    patched_meta_files.set_configs(mkdocs_config=mkdocs_config, meta_plugin_config=pub_meta_plugin.config)

    meta_dir: MetaFile = MetaFile(
        path=Path("docs"),
        abs_path=Path("/Users/docs/README.md"),
        is_dir=True,
    )
    with patch.object(Path, "exists", return_value=True):
        patched_meta_files["docs"] = meta_dir

    if with_meta_file:
        meta_file: MetaFile = MetaFile(
            path=Path(path),
            abs_path=Path(f"/Users/docs/{'index.md' if path == '.' else path}"),
            is_dir=False,
        )
        with patch.object(Path, "exists", return_value=True):
            patched_meta_files[path] = meta_file
        meta_file.is_draft = is_draft

    files = Files(
        [
            File(
                path=path,
                src_dir="/Users/docs",
                dest_dir="/Users/site",
                use_directory_urls=True,
            ),
        ],
    )

    new_files = patched_meta_files.change_files_slug(
        files=files,
        ignored_dirs=[Path(ignored_dir)] if ignored_dir else [],
    )
    new_file = new_files.get_file_from_path(path)
    if expected_url:
        check.equal(expected_url, new_file.url)
    else:
        check.is_none(new_file)
