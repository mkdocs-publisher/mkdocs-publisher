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
from datetime import datetime
from datetime import timezone
from math import ceil
from pathlib import Path
from typing import Any
from typing import Generator  # noqa: UP035

import yaml
from mkdocs.config.defaults import MkDocsConfig

from mkdocs_publisher._shared import links
from mkdocs_publisher._shared import mkdocs_utils
from mkdocs_publisher._shared import publisher_utils
from mkdocs_publisher._shared import templates
from mkdocs_publisher._shared.config_enums import PublishChoiceEnum
from mkdocs_publisher.blog.config import BlogPluginConfig
from mkdocs_publisher.meta.config import MetaPluginConfig

log = logging.getLogger("mkdocs.publisher.blog.blog_files")


@dataclass
class BlogFile(publisher_utils.PublisherFile):
    temp_path: Path | None = field(default=None)
    abs_temp_path: Path | None = field(default=None)
    teaser: str | None = field(default=None, repr=False)
    date_created: float | None = field(default=None)
    date_updated: float | None = field(default=None)
    read_time_sec: int | None = field(default=None)
    tags: list[str] = field(default_factory=list)
    categories: list[str] = field(default_factory=list)


class BlogFiles(publisher_utils.PublisherFiles):
    def __init__(self) -> None:
        self._abs_blog_path: Path | None = None
        self._abs_blog_temp_path: Path | None = None
        self._dir_meta_file: str = "README.md"
        self._nav: list[dict[str, str]] = []
        self._on_serve: bool = False

        super().__init__()

    @property
    def nav(self) -> list[dict]:
        return self._nav

    @property
    def abs_blog_path(self) -> Path | None:
        return self._abs_blog_path

    @property
    def abs_blog_temp_path(self) -> Path | None:
        return self._abs_blog_temp_path

    @property
    def blog_temp_path(self) -> Path | None:
        return self._abs_blog_temp_path.relative_to(Path(self._mkdocs_config.docs_dir))

    def remove_old_temp_dirs(self, mkdocs_config: MkDocsConfig) -> None:
        """Remove old temporary directories and files"""
        old_temps = Path(mkdocs_config.docs_dir).glob("**/*_pub_blog")
        for old_temp in old_temps:
            shutil.rmtree(str(old_temp), ignore_errors=True)

    def remove_temp_dirs(self) -> None:
        """Remove temporary directories and files"""
        shutil.rmtree(str(self._abs_blog_temp_path), ignore_errors=True)

    def set_configs(
        self,
        mkdocs_config: MkDocsConfig,
        meta_plugin_config: MetaPluginConfig | None,
        blog_plugin_config: BlogPluginConfig | None,
    ) -> None:
        super().set_configs(
            mkdocs_config=mkdocs_config,
            meta_plugin_config=meta_plugin_config,
            blog_plugin_config=blog_plugin_config,
        )

        # Create a new temporary directory
        self._abs_blog_path = Path(self._mkdocs_config.docs_dir) / Path(self._blog_plugin_config.blog_dir)
        self._abs_blog_temp_path = Path(
            tempfile.mkdtemp(
                prefix=f"{self._blog_plugin_config.blog_dir}_",
                suffix="_pub_blog",
                dir=Path(self._mkdocs_config.docs_dir),
            ),
        )

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

    def _get_title(self, blog_file: BlogFile, meta: dict[str, Any]) -> None:
        title_key_name = self._blog_plugin_config.title.key_name
        if meta.get(title_key_name, "") == "":
            log.critical(f"{blog_file.path.name} doesn't contain '{title_key_name}' or title is empty")

        blog_file.title = meta.get(title_key_name)

    def _get_slug(self, blog_file: BlogFile, meta: dict[str, Any]) -> None:
        """Calculate slug for given file"""
        blog_file.slug = links.create_slug(  # pragma: no cover
            file_name=blog_file.path.stem,
            slug_mode=self._meta_plugin_config.slug.mode,
            slug=meta.get(self._blog_plugin_config.slug.key_name),
            title=blog_file.title,
            warn_on_missing=self._blog_plugin_config.slug.warn_on_missing,
        )

    def _get_categories(self, blog_file: BlogFile, meta: dict[str, Any]) -> None:
        """Get categories from metadata"""
        blog_file.categories = meta.get(self._blog_plugin_config.categories.key_name, [])
        if self._on_serve and not blog_file.categories:
            blog_file.categories = ["missing"]
        if self._blog_plugin_config.categories.warn_on_missing and not blog_file.categories:
            log.warning(
                f"{blog_file.path.name} doesn't contain categories"
                f" (key name: '{self._blog_plugin_config.categories.key_name}')",
            )

    def _get_tags(self, blog_file: BlogFile, meta: dict[str, Any]) -> None:
        """Get tags from metadata"""
        blog_file.tags = meta.get(self._blog_plugin_config.tags.key_name, [])
        if self._on_serve and not blog_file.tags:
            blog_file.tags = ["missing"]
        if self._blog_plugin_config.tags.warn_on_missing and not blog_file.tags:
            log.warning(
                f"{blog_file.path.name} doesn't contain tags"
                f" (key name: '{self._blog_plugin_config.tags.key_name}')",
            )

    def _get_published_status(self, blog_file: BlogFile, meta: dict[str, Any]) -> None:
        publish = meta.get(str(self._blog_plugin_config.publish.key_name), None)

        # Get default values if publish status is not specified
        if publish is None:
            publish = self._blog_plugin_config.publish.default
            if self._blog_plugin_config.publish.warn_on_missing:
                log.warning(
                    f'Missing "{self._meta_plugin_config.publish.key_name}" value in '
                    f'file "{blog_file.path}". Setting to default value: "{publish}".',
                )

        # Set values depends on publish status
        if publish == PublishChoiceEnum.HIDDEN.name:
            blog_file.is_hidden = True
            blog_file.is_draft = False
        elif publish in PublishChoiceEnum.published() or self._on_serve:
            blog_file.is_hidden = False
            blog_file.is_draft = False
        else:
            blog_file.is_hidden = False
            blog_file.is_draft = True

        if publish not in PublishChoiceEnum.choices():
            publish = self._meta_plugin_config.publish.file_default
            log.warning(
                f'Wrong key "{self._blog_plugin_config.publish.key_name}" value ({publish}) '
                f'in file "{blog_file.path}" (only {PublishChoiceEnum.choices()} are possible)',
            )

    def _get_dates(self, blog_file: BlogFile, meta: dict[str, Any]) -> None:
        date_created = meta.get(str(self._blog_plugin_config.posts.date_created_key_name), None)
        date_updated = meta.get(str(self._blog_plugin_config.posts.date_updated_key_name), None)

        if date_updated is None:
            blog_file.date_updated = datetime.now(tz=timezone.utc).timestamp()
        else:
            try:
                blog_file.date_updated = datetime.strptime(
                    str(date_updated),
                    self._blog_plugin_config.posts.date_created_md_format,
                ).timestamp()
            except ValueError as e:
                log.critical(
                    f"{blog_file.path.name} '{self._blog_plugin_config.posts.date_created_key_name}'"
                    f" date format is incorrect (error: {e})",
                )

        if date_created is None:
            log.warning(
                f'Missing "{self._blog_plugin_config.posts.date_created_md_format}" value in file "{blog_file.path}".',
            )
        else:
            try:
                blog_file.date_created = (
                    datetime.strptime(
                        str(date_created),
                        self._blog_plugin_config.posts.date_updated_md_format,
                    )
                    .replace(tzinfo=timezone.utc)
                    .timestamp()
                )
            except ValueError as e:
                log.critical(
                    f"{blog_file.path.name} '{self._blog_plugin_config.posts.date_updated_key_name}'"
                    f" date format is incorrect (error: {e})",
                )

    def _get_metadata(self, blog_file: BlogFile) -> None:
        """Read all metadata values for given file"""
        markdown, meta = mkdocs_utils.read_md_file(md_file_path=blog_file.abs_path)
        self._get_teaser(blog_file=blog_file, markdown=markdown)
        self._get_reading_time(blog_file=blog_file, markdown=markdown)
        self._get_published_status(blog_file=blog_file, meta=meta)

        if not blog_file.is_draft:
            self._get_categories(blog_file=blog_file, meta=meta)
            self._get_tags(blog_file=blog_file, meta=meta)
            self._get_title(blog_file=blog_file, meta=meta)
            self._get_slug(blog_file=blog_file, meta=meta)
            self._get_dates(blog_file=blog_file, meta=meta)
        # TODO: log drafts and hidden files

    def __setitem__(self, path: str, blog_file: BlogFile) -> None:
        """Add file"""
        if str(blog_file.path.name) != self._dir_meta_file:
            self._get_metadata(blog_file=blog_file)

            super().__setitem__(path, blog_file)
        # TODO: read some config from README.md

    def generator(self) -> Generator[BlogFile, Any, None]:
        """Blog files generator used for building navigation"""

        timestamped_files = {blog_file.date_created: blog_file for blog_file in self.values() if not blog_file.is_draft}
        ordered_values = [timestamped_files[timestamp] for timestamp in sorted(timestamped_files.keys(), reverse=True)]

        for blog_file in ordered_values:
            blog_file: BlogFile
            yield blog_file

    def _write_post(self, file_name: Path, meta: dict, posts: list[str]) -> None:
        file_path = self._abs_blog_temp_path.joinpath(file_name)
        with file_path.open(mode="w") as index_file:
            index_file.write(f"---\n{yaml.dump(meta, default_flow_style=False, sort_keys=False)}---")
            for post in posts:
                index_file.write(post)
            self._nav.append({meta["title"]: str(file_path.relative_to(self._mkdocs_config.docs_dir))})

    def generate_posts(self) -> None:
        self.abs_blog_temp_path.joinpath(Path(self._blog_plugin_config.posts.slug)).mkdir(parents=True, exist_ok=True)
        for blog_file in self.generator():
            if not blog_file.is_draft:
                file_name = blog_file.abs_path.relative_to(str(self.abs_blog_path))
                blog_file.abs_temp_path = self.abs_blog_temp_path.joinpath(
                    Path(self._blog_plugin_config.posts.slug).joinpath(file_name),
                )

                blog_file.temp_path = self.blog_temp_path.joinpath(
                    Path(self._blog_plugin_config.posts.slug).joinpath(file_name),
                )
                self._nav.append({str(blog_file.title): str(blog_file.temp_path)})
                shutil.copy(blog_file.abs_path, blog_file.abs_temp_path)

    def generate_indexes(self) -> None:
        """Generate blog teasers"""

        index: int = 0
        posts: list = []
        for blog_file in self.generator():
            if not blog_file.is_hidden:
                blog_post_context = {
                    "blog_file": blog_file,
                    "blog_slug": str(self._blog_plugin_config.blog_slug),
                    "date_created": datetime.fromtimestamp(
                        timestamp=blog_file.date_created,  # type: ignore[reportArgumentType]
                        tz=timezone.utc,
                    ).strftime(self._blog_plugin_config.posts.date_created_display_format),
                    "date_updated": datetime.fromtimestamp(
                        timestamp=blog_file.date_updated,  # type: ignore[reportArgumentType]
                        tz=timezone.utc,
                    ).strftime(self._blog_plugin_config.posts.date_updated_display_format),
                    "site_url": str(self._mkdocs_config.site_url),
                    "tags_slug": str(self._blog_plugin_config.tags.slug),
                }

                posts.append(templates.render(tpl_file="blog-posts.html", context=blog_post_context))

                # Trigger a new page creation every `posts_per_page` posts
                if len(posts) % self._blog_plugin_config.index.posts_per_page == 0:
                    meta = {
                        "title": f"Blog{'' if index == 0 else f' - page {index}'}",
                        "slug": f"{'.' if index == 0 else index}",
                        "publish": True,
                        "search": self._blog_plugin_config.index.searchable,
                    }
                    self._write_post(file_name=Path(f"{'index' if index == 0 else index}.md"), meta=meta, posts=posts)
                    posts.clear()
                    index += 1

        # Create a new page for any remaining posts that didn't fill up the last page
        if len(posts) > 0:
            meta = {
                "title": f"Blog{'' if index == 0 else f' - page {index}'}",
                "slug": f"{'.' if index == 0 else index}",
                "publish": True,
                "search": self._blog_plugin_config.index.searchable,
            }
            self._write_post(file_name=Path(f"{'index' if index == 0 else index}.md"), meta=meta, posts=posts)

    def get_by_temp_file(self, temp_path: Path | None = None, abs_temp_path: Path | None = None) -> BlogFile | None:
        if temp_path is not None and abs_temp_path is not None:
            msg = "Provide only one attribute, either 'temp_path' or 'abs_temp_path'"
            raise ValueError(msg)

        if temp_path is None:
            temp_path = abs_temp_path.relative_to(str(self._abs_blog_temp_path))

        return self.get(str(temp_path).replace(str(self.blog_temp_path), self._blog_plugin_config.blog_dir), None)
