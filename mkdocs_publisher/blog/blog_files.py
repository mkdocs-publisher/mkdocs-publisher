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
import tempfile
from collections import UserDict
from dataclasses import dataclass
from dataclasses import field
from pathlib import Path
from typing import Optional
from typing import cast

from mkdocs.config.defaults import MkDocsConfig

from mkdocs_publisher._shared import mkdocs_utils
from mkdocs_publisher.blog.config import BlogPluginConfig
from mkdocs_publisher.meta.config import MetaPluginConfig

log = logging.getLogger("mkdocs.publisher.blog.blog_files")


@dataclass
class BlogFile:
    path: Path
    abs_path: Path = field(repr=False)
    is_meta: bool = field(default=False)
    teaser: Optional[str] = field(default=None, repr=False)
    markdown: Optional[str] = field(default=None, repr=False)
    date_created: Optional[int] = field(default=None)
    date_updated: Optional[int] = field(default=None)
    tags: list[str] = field(default_factory=lambda: [])
    categories: list[str] = field(default_factory=lambda: [])


class BlogFiles(UserDict):
    def __init__(self):
        self._on_serve: bool = False
        self._mkdocs_config: Optional[MkDocsConfig] = None
        self._blog_plugin_config: Optional[BlogPluginConfig] = None
        self._meta_plugin_config: Optional[MetaPluginConfig] = None
        self._abs_blog_path: Optional[Path] = None
        self._abs_blog_temp_path: Optional[Path] = None
        self._dir_meta_file: str = "README.md"
        super().__init__()

    @property
    def on_serve(self) -> bool:
        return self._on_serve

    @on_serve.setter
    def on_serve(self, on_serve: bool):
        self._on_serve = on_serve

    def remove_temp_dirs(self):
        """Remove file"""
        # shutil.rmtree(self._abs_blog_temp_path, ignore_errors=True)

    def set_configs(self, mkdocs_config: MkDocsConfig, blog_plugin_config: BlogPluginConfig):
        self._mkdocs_config = mkdocs_config
        self._blog_plugin_config = blog_plugin_config
        self._abs_blog_path = Path(self._mkdocs_config.docs_dir) / Path(self._blog_plugin_config.blog_dir)
        self._abs_blog_temp_path = Path(tempfile.mkdtemp(prefix=".pub_blog_", dir=Path(self._mkdocs_config.docs_dir)))
        self._meta_plugin_config = cast(
            MetaPluginConfig, mkdocs_utils.get_plugin_config(mkdocs_config=self._mkdocs_config, plugin_name="pub-meta")
        )
        if self._meta_plugin_config:
            self._dir_meta_file = self._meta_plugin_config.dir_meta_file

    def add_blog_files(self):
        """Iterate over all files and directories in blog subdirectory"""
        for docs_file in sorted(self._abs_blog_path.glob("**/*.md")):
            blog_file = BlogFile(
                path=docs_file.relative_to(self._mkdocs_config.docs_dir),
                abs_path=docs_file,
                is_meta=docs_file.name == self._dir_meta_file,
            )
            self[str(blog_file.path)] = blog_file

    def _get_metadata(self, blog_file: BlogFile, blog_file_path: Path):  # pragma: no cover
        """Read all metadata values for given file"""

        markdown, meta = mkdocs_utils.read_md_file(md_file_path=blog_file_path)
        _ = markdown
        log.critical(meta)

    def __setitem__(self, path: str, blog_file: BlogFile):
        """Add file"""
        self._get_metadata(blog_file=blog_file, blog_file_path=blog_file.abs_path)

        super().__setitem__(path, blog_file)
