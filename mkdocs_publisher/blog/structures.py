from dataclasses import asdict
from dataclasses import dataclass
from dataclasses import field
from datetime import datetime
from pathlib import Path
from typing import Dict
from typing import List
from typing import Optional

from mkdocs.config.defaults import MkDocsConfig

from mkdocs_publisher._common import mkdocs_utils
from mkdocs_publisher.blog.config import BlogPluginConfig
from mkdocs_publisher.meta.config import MetaPluginConfig


@dataclass
class BlogPost:
    """Single blog post data container"""

    title: str
    date: datetime
    path: Optional[str]
    content: Optional[str]
    tags: Optional[List[str]]
    categories: Optional[List[str]]
    slug: Optional[str] = None
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
    meta_config: Optional[MetaPluginConfig] = field(init=False, default=None)
    translation: Translation = field(init=False)
    temp_dir: Path = field(init=False)
    docs_dir: Path = field(init=False)
    blog_dir: Path = field(init=False)
    site_dir: Path = field(init=False)
    blog_posts: Dict[datetime, BlogPost] = field(init=False, default_factory=lambda: dict())
    temp_files: Dict[str, Path] = field(init=False, default_factory=lambda: dict())

    @property
    def temp_files_list(self) -> List[str]:
        temp_files = []
        for path in self.temp_files.values():
            temp_files.append(str(path.relative_to(self.temp_dir)))
        return temp_files

    def parse_configs(self, mkdocs_config: MkDocsConfig, plugin_config: BlogPluginConfig):
        from mkdocs_publisher.blog.translate import Translate

        self.mkdocs_config = mkdocs_config
        self.plugin_config = plugin_config
        self.meta_config: Optional[MetaPluginConfig] = mkdocs_utils.get_plugin_config(
            mkdocs_config=mkdocs_config, plugin_name="pub-meta"
        )  # type: ignore
        self.temp_dir = Path(plugin_config.temp_dir)
        self.docs_dir = Path(mkdocs_config.docs_dir)
        self.blog_dir = Path(plugin_config.blog_dir)
        self.site_dir = Path(mkdocs_config.site_dir)
        self.translation = Translate(config=plugin_config).translation

        self.temp_dir.mkdir(exist_ok=True)
