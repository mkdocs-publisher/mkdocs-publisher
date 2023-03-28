import logging
import re
from pathlib import Path
from typing import List
from typing import Optional
from typing import cast

import frontmatter
from mkdocs.config import Config
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.plugins import BasePlugin
from mkdocs.plugins import event_priority
from mkdocs.structure.files import Files
from mkdocs.structure.nav import Link
from mkdocs.structure.nav import Navigation
from mkdocs.structure.nav import Section
from mkdocs.structure.pages import Page

from mkdocs_publisher import _utils
from mkdocs_publisher.auto_nav.config import AutoNavPluginConfig

log = logging.getLogger("mkdocs.plugins.publisher.auto-nav")


class AutoNavPlugin(BasePlugin[AutoNavPluginConfig]):
    def __init__(self):
        from mkdocs_publisher.blog.config import BlogPluginConfig

        self.blog_config: Optional[BlogPluginConfig] = None

    def _read_markdown_title(self, file: Path) -> str:
        with open(file) as file_meta:
            post = frontmatter.load(file_meta)
        if "title" not in post.metadata:
            log.warning(f"File '{file}' doesn't contain 'title' meta data")
        return post.get("title", default=file.stem)

    def _iterate_dir(self, directory: Path, skip_subfiles_of_dir: List[str], relative_to: Path):
        nav = list()
        sorted_files = sorted([f for f in directory.glob("**/*")])

        # Make index.md a first file in give directory
        no_index_files = [f for f in sorted_files if f.name != "index.md"]
        sorted_files = [f for f in sorted_files if f.name == "index.md"]
        sorted_files.extend(no_index_files)

        for file in sorted_files:
            if not any([s for s in skip_subfiles_of_dir if str(file).startswith(s)]):
                if file.is_dir():
                    meta_file = file / self.config.meta_file_name
                    if meta_file.exists():
                        with open(meta_file) as file_meta:
                            post = frontmatter.load(file_meta)
                    else:
                        post = {"title": file.stem}
                    title = post.get("title")
                    subdir_nav = {
                        title: self._iterate_dir(
                            directory=file,
                            skip_subfiles_of_dir=skip_subfiles_of_dir,
                            relative_to=relative_to,
                        )
                    }
                    if list(subdir_nav.values())[0]:
                        nav.append(subdir_nav)
                elif (
                    file.is_file()
                    and len(file.relative_to(directory).parents) == 1
                    and file.suffix == ".md"
                ):
                    if Path(file).parts[-1] != self.config.meta_file_name:
                        title = self._read_markdown_title(file=file)
                        nav.append({title: str(file.relative_to(relative_to))})
                else:
                    log.debug(f"{file} is not .md or dir and will not be added to navigation")
            elif file.suffix == ".md" and not any(
                [p for p in [str(p) for p in file.parents][0:-1] if p in skip_subfiles_of_dir]
            ):
                title = self._read_markdown_title(file=file)
                nav.append({title: str(file.relative_to(relative_to))})
            elif (
                file.is_dir()
                and self.blog_config is not None
                and str(file).endswith(self.blog_config.blog_dir)
            ):
                nav.append({file.stem: str(file.relative_to(relative_to))})
        return nav

    @event_priority(100)  # Run before any other plugins
    def on_config(self, config: MkDocsConfig) -> Optional[Config]:
        from blog.config import BlogPluginConfig
        from blog.plugin import BlogPlugin

        self.blog_config = cast(
            BlogPluginConfig,
            _utils.get_plugin_config(
                plugin=BlogPlugin(),
                config_file_path=str(self.config.config_file_path),
                yaml_config_key="pub-blog",
            ),
        )
        if self.blog_config is not None:
            blog_dir = str(Path(config.docs_dir) / Path(self.blog_config.blog_dir))
            if blog_dir not in self.config.skip_dir:
                self.config.skip_dir.append(blog_dir)

        skip_subfiles_of_dir = [str(Path(f)) for f in self.config.skip_dir]
        nav = self._iterate_dir(
            directory=Path(config.docs_dir),
            skip_subfiles_of_dir=skip_subfiles_of_dir,
            relative_to=Path(config.docs_dir),
        )
        config.nav = nav

        return config

    def _iterate_nav(self, items):
        nav = []
        for item in items:
            if (
                isinstance(item, Page)
                and Path(item.file.src_path).parts[-1] != self.config.meta_file_name
            ):
                nav.append(item)
            elif isinstance(item, Section):
                item.children = self._iterate_nav(items=item.children)
                nav.append(item)
            elif isinstance(item, Link) and item.url.split("/")[-1] != self.config.meta_file_name:
                nav.append(item)
        return nav

    def on_nav(
        self, nav: Navigation, *, config: MkDocsConfig, files: Files
    ) -> Optional[Navigation]:

        nav.items = self._iterate_nav(items=nav.items)

        return nav

    # @event_priority(100)  # Run before any other plugins
    def on_files(self, files: Files, *, config: MkDocsConfig) -> Optional[Files]:
        if self.config.remove_sort_prefix_from_slug:
            prefix = rf"^[0-9]+{self.config.sort_prefix_delimiter}"
            new_files = Files([])
            for file in files:
                file.dest_path = str(
                    Path(*[re.sub(prefix, "", part) for part in Path(file.dest_path).parts])
                )
                file.url = str(Path(*[re.sub(prefix, "", part) for part in Path(file.url).parts]))
                abs_dest_path = Path(
                    *[
                        re.sub(prefix, "", part)
                        for part in Path(file.abs_dest_path).relative_to(config.site_dir).parts
                    ]
                )
                file.abs_dest_path = str(Path(config.site_dir) / abs_dest_path)
                if Path(file.src_path).parts[-1] != self.config.meta_file_name:
                    new_files.append(file)
            return new_files
        return files
