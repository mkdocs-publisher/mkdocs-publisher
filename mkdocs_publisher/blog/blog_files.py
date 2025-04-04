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
import shutil
import tempfile
from dataclasses import dataclass
from dataclasses import field
from math import ceil
from pathlib import Path

from mkdocs.config.defaults import MkDocsConfig

from mkdocs_publisher._shared import mkdocs_utils
from mkdocs_publisher._shared import publisher_utils
from mkdocs_publisher.blog.config import BlogPluginConfig
from mkdocs_publisher.meta.config import MetaPluginConfig

log = logging.getLogger("mkdocs.publisher.blog.blog_files")


@dataclass
class BlogFile(publisher_utils.PublisherFile):
    teaser: str | None = field(default=None, repr=False)
    markdown: str | None = field(default=None, repr=False)
    date_created: int | None = field(default=None)
    date_updated: int | None = field(default=None)
    read_time_sec: int | None = field(default=None)
    tags: list[str] = field(default_factory=list)
    categories: list[str] = field(default_factory=list)


class BlogFiles(publisher_utils.PublisherFiles):
    def __init__(self) -> None:
        self._blog_plugin_config: BlogPluginConfig | None = None
        self._abs_blog_path: Path | None = None
        self._abs_blog_temp_path: Path | None = None
        self._dir_meta_file: str = "README.md"

        super().__init__()

    def remove_temp_dirs(self) -> None:
        """Remove temporary files"""
        shutil.rmtree(str(self._abs_blog_temp_path), ignore_errors=True)

    def set_configs(self, mkdocs_config: MkDocsConfig, blog_plugin_config: BlogPluginConfig) -> None:
        super().set_configs(
            mkdocs_config=mkdocs_config,
            meta_plugin_config=mkdocs_utils.get_plugin_config(
                plugin_config_type=MetaPluginConfig,  # type: ignore[reportArgumentType]
                mkdocs_config=mkdocs_config,
            ),
        )

        self._blog_plugin_config = blog_plugin_config
        self._abs_blog_path = Path(self._mkdocs_config.docs_dir) / Path(self._blog_plugin_config.blog_dir)
        self._abs_blog_temp_path = Path(tempfile.mkdtemp(prefix=".pub_blog_", dir=Path(self._mkdocs_config.docs_dir)))

        if self._meta_plugin_config:
            self._dir_meta_file = self._meta_plugin_config.dir_meta_file

    def add_blog_files(self) -> None:
        """Iterate over all files and directories in blog subdirectory"""
        for docs_file in sorted(self._abs_blog_path.glob("**/*.md")):
            blog_file = BlogFile(
                path=docs_file.relative_to(self._mkdocs_config.docs_dir),
                abs_path=docs_file,
                is_dir=docs_file.name == self._dir_meta_file,
            )
            self[str(blog_file.path)] = blog_file

    def list_blog_files(self) -> None:
        for f in self:
            log.warning(f)

    def _get_teaser(self, blog_file: BlogFile, markdown: str) -> None:
        teaser_lines = []
        for line in markdown.split("\n"):
            teaser_lines.append(line)
            if line == self._blog_plugin_config.posts.teaser_separator:
                blog_file.teaser = "\n".join(teaser_lines)

    def _get_reading_time(self, blog_file: BlogFile, markdown: str) -> None:
        blog_file.read_time_sec = ceil(
            mkdocs_utils.count_words(markdown) * 60 / self._blog_plugin_config.posts.words_per_minute,
        )

    def _get_metadata(self, blog_file: BlogFile) -> None:
        """Read all metadata values for given file"""
        markdown, meta = mkdocs_utils.read_md_file(md_file_path=blog_file.abs_path)
        self._get_teaser(blog_file=blog_file, markdown=markdown)
        self._get_reading_time(blog_file=blog_file, markdown=markdown)

        # TODO: add published status read
        _ = meta

        """
        self._get_publish_status(meta_file=meta_file, meta=meta)
        self._get_title(meta_file=meta_file, meta=meta, markdown=markdown)
        self._get_slug(meta_file=meta_file, meta=meta)
        """

    def __setitem__(self, path: str, blog_file: BlogFile) -> None:
        """Add file"""
        self._get_metadata(blog_file=blog_file)

        super().__setitem__(path, blog_file)
