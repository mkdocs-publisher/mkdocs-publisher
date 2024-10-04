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

from dataclasses import asdict
from dataclasses import dataclass
from dataclasses import field
from datetime import datetime
from pathlib import Path

from mkdocs.config.defaults import MkDocsConfig

from mkdocs_publisher._shared import mkdocs_utils
from mkdocs_publisher.blog.config import BlogPluginConfig
from mkdocs_publisher.meta.config import MetaPluginConfig


@dataclass
class BlogPost:
    """Single blog post data container"""

    title: str
    date: datetime
    path: str | None
    content: str | None
    tags: list[str] | None
    categories: list[str] | None
    slug: str | None = None
    teaser: str = ""
    is_teaser: bool = False

    @property
    def as_dict(self) -> dict:
        return asdict(self)


@dataclass
class Translation:
    teaser_link_text: str
    blog_page_title: str
    blog_navigation_name: str
    recent_blog_posts_navigation_name: str
    archive_page_title: str
    archive_navigation_name: str
    categories_page_title: str
    categories_navigation_name: str
    tags_page_title: str
    tags_navigation_name: str
    newer_posts: str
    older_posts: str

    @property
    def as_dict(self) -> dict:
        return asdict(self)


@dataclass
class BlogConfig:
    mkdocs_config: MkDocsConfig = field(init=False)
    plugin_config: BlogPluginConfig = field(init=False)
    meta_config: MetaPluginConfig | None = field(init=False, default=None)
    translation: Translation = field(init=False)
    temp_dir: Path = field(init=False)
    docs_dir: Path = field(init=False)
    blog_dir: Path = field(init=False)
    site_dir: Path = field(init=False)
    blog_posts: dict[datetime, BlogPost] = field(init=False, default_factory=lambda: dict())
    temp_files: dict[str, Path] = field(init=False, default_factory=lambda: dict())

    @property
    def temp_files_list(self) -> list[str]:
        temp_files = []
        for path in self.temp_files.values():
            temp_files.append(str(path.relative_to(self.temp_dir)))
        return temp_files

    def parse_configs(self, mkdocs_config: MkDocsConfig, plugin_config: BlogPluginConfig):
        from mkdocs_publisher.blog.translate import Translate

        self.mkdocs_config = mkdocs_config
        self.plugin_config = plugin_config
        self.meta_config: MetaPluginConfig | None = (
            mkdocs_utils.get_plugin_config(mkdocs_config=mkdocs_config, plugin_name="pub-meta") or None
        )  # type: ignore
        self.temp_dir = Path(plugin_config.temp_dir)
        self.docs_dir = Path(mkdocs_config.docs_dir)
        self.blog_dir = Path(plugin_config.blog_dir)
        self.site_dir = Path(mkdocs_config.site_dir)
        self.translation = Translate(config=plugin_config).translation

        self.temp_dir.mkdir(exist_ok=True)
