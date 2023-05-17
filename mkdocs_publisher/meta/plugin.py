import logging
from datetime import datetime
from pathlib import Path
from typing import Optional
from typing import cast

from mkdocs.config import Config
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.plugins import BasePlugin
from mkdocs.plugins import event_priority
from mkdocs.structure.files import Files
from mkdocs.structure.nav import Link
from mkdocs.structure.nav import Navigation
from mkdocs.structure.nav import Section
from mkdocs.structure.pages import Page
from mkdocs.utils import meta as meta_parser

from mkdocs_publisher.blog.config import BlogPluginConfig
from mkdocs_publisher.meta.config import MetaPluginConfig
from mkdocs_publisher.obsidian.config import ObsidianPluginConfig

log = logging.getLogger("mkdocs.plugins.publisher.meta")
INDEX_FILE_NAME = "index.md"


class MetaPlugin(BasePlugin[MetaPluginConfig]):
    def __init__(self):
        self._dirs_slugs: dict = {}
        self._dirs_titles: dict = {}
        self._skip_dirs: list = []
        self._not_other_files: list = []
        self._blog_config: BlogPluginConfig = cast(BlogPluginConfig, None)
        self._draft_files: list = []
        self._hidden_files: list = []

    def _build_config_nav(self, directory: Path, relative_to: Path) -> list:
        nav = list()
        sorted_files = sorted([f for f in directory.glob("*")])

        # Make index.md a first file in give directory
        other_files = [f for f in sorted_files if f.name not in self._not_other_files]
        sorted_files = [f for f in sorted_files if f.name == "index.md"]
        sorted_files.extend(other_files)

        for file in sorted_files:
            if not any([s for s in self._skip_dirs if str(file).startswith(str(s))]):
                if file.is_dir():
                    title = self._dirs_titles.get(file, file.stem)
                    nav.append(
                        {title: self._build_config_nav(directory=file, relative_to=relative_to)}
                    )
                elif file.is_file() and file.suffix == ".md":
                    with file.open(encoding="utf-8-sig", errors="strict") as md_file:
                        markdown, meta = meta_parser.get_data(md_file.read())
                        title = meta.get(self.config.title.key_name, file.stem)

                        # Read document status
                        status = meta.get(self.config.status.key_name)
                        if status is None:
                            if self.config.status.warn_on_missing:
                                log.warning(
                                    f'Missing "{self.config.status.key_name}" value in '
                                    f'file "{file.relative_to(relative_to)}". Setting to '
                                    f'default value: "{self.config.status.default}".'
                                )
                            status = self.config.status.default

                        if status == "draft":
                            self._draft_files.append(str(file.relative_to(relative_to)))
                        elif status == "hidden":
                            self._hidden_files.append(str(file.relative_to(relative_to)))

                        if status != "draft":
                            nav.append({title: str(file.relative_to(relative_to))})
            elif (
                file.is_dir()
                and self._blog_config is not None
                and str(file.relative_to(relative_to)) == self._blog_config.blog_dir
            ):
                nav.append({file.stem: str(file.relative_to(relative_to))})
        return nav

    def _nav_cleanup(self, items: list, elements_to_remove: list) -> list:

        nav = []
        for item in items:
            if isinstance(item, Page) and item.file.src_uri not in elements_to_remove:
                nav.append(item)
            elif isinstance(item, Link):
                nav.append(item)
            elif isinstance(item, Section):
                item.children = self._nav_cleanup(
                    items=item.children, elements_to_remove=elements_to_remove
                )
                if len(item.children) > 0:  # Skip empty Sections
                    nav.append(item)

        return nav

    @event_priority(100)  # Run before any other plugins
    def on_config(self, config: MkDocsConfig) -> Optional[Config]:

        # Setup some default values
        self._skip_dirs = cast(list, self.config.skip.dirs)
        self._not_other_files = [INDEX_FILE_NAME, self.config.meta_file_name]

        log.info(f'Reading meta data from "{self.config.meta_file_name}" files')
        for meta_file in Path(config.docs_dir).glob(f"**/{self.config.meta_file_name}"):
            with meta_file.open(encoding="utf-8-sig", errors="strict") as md_file:
                markdown, meta = meta_parser.get_data(md_file.read())

                # Read slug for directories
                slug = meta.get(self.config.slug.key_name)
                if slug is not None:
                    self._dirs_slugs[meta_file.parent] = slug

                # Read title for directory
                title = meta.get(self.config.title.key_name)
                if title is not None:
                    self._dirs_titles[meta_file.parent] = title

                # Read skipped directories
                skip_dir = meta.get(self.config.skip.key_name)
                if skip_dir:
                    self._skip_dirs.append(str(meta_file.parent.relative_to(config.docs_dir)))
                elif skip_dir is not None:
                    log.warning(
                        f'Wrong key "{self.config.skip.key_name}" value '
                        f'in file "{meta_file.relative_to(config.docs_dir)}"'
                        f'(only "true" and "false" are possible)'
                    )

        # Add blog dir to one that will be skipped (blog has it's own order resolution)
        self._blog_config: BlogPluginConfig = config.plugins["pub-blog"].config
        if self._blog_config is not None:
            if self._blog_config.blog_dir not in self._skip_dirs:
                self._skip_dirs.append(self._blog_config.blog_dir)

        # Add obsidian dirs to ones that will be skipped
        obsidian_config: ObsidianPluginConfig = config.plugins["pub-obsidian"].config
        if obsidian_config is not None:
            if obsidian_config.obsidian_dir not in self._skip_dirs:
                self._skip_dirs.append(obsidian_config.obsidian_dir)
            if obsidian_config.templates_dir not in self._skip_dirs:
                self._skip_dirs.append(obsidian_config.templates_dir)

        log.info(f"Skipping directories: {self._skip_dirs}")
        self._skip_dirs = [Path(config.docs_dir) / f for f in self._skip_dirs]

        for skip_dir in self._skip_dirs:
            if not skip_dir.exists():
                log.warning(
                    f'Directory "{skip_dir.relative_to(config.docs_dir)}" '
                    f"doesn't exists and cannot be skipped"
                )
        config.nav = self._build_config_nav(
            directory=Path(config.docs_dir), relative_to=Path(config.docs_dir)
        )

        log.info(f"Draft files: {self._draft_files}")
        log.info(f"Hidden files: {self._hidden_files}")

    def on_files(self, files: Files, *, config: MkDocsConfig) -> Optional[Files]:

        relative_skip_dirs = [str(f.relative_to(config.docs_dir)) for f in self._skip_dirs]
        if self._blog_config is not None:
            relative_skip_dirs.remove(self._blog_config.blog_dir)

        new_files = Files(files=[])
        for file in files:
            if (
                not any([file.src_uri.startswith(skip_dir) for skip_dir in relative_skip_dirs])
                and str(Path(file.src_uri).name) != self.config.meta_file_name
                and str(file.src_uri) not in self._draft_files
            ):
                new_files.append(file)

        return new_files

    def on_nav(
        self, nav: Navigation, *, config: MkDocsConfig, files: Files
    ) -> Optional[Navigation]:

        elements_to_remove = []
        elements_to_remove.extend(self._draft_files)
        elements_to_remove.extend(self._hidden_files)

        nav.items = self._nav_cleanup(items=nav.items, elements_to_remove=elements_to_remove)

        return nav

    def on_page_markdown(self, markdown: str, *, page: Page, config: MkDocsConfig, files: Files):

        # Read slug
        slug = page.meta.get(self.config.slug.key_name)
        if slug is None and self.config.slug.warn_on_missing:
            log.warning(
                f'File "{page.file.src_path}" has no "{self.config.slug.key_name}" meta data'
            )

        # Get URL parts
        if page.file.url.endswith("/"):
            page.file.url = page.file.url[0:-1]
        url_parts = page.file.url.split("/")

        # Get abs file parts
        path_parts: list[Path] = []
        for path_part in page.file.src_path.split("/"):
            if not path_parts:
                path_parts.append(Path(config.docs_dir) / path_part)
            else:
                path_parts.append(path_parts[-1] / path_part)

        # Replace URL parts that have slug defined
        for position, path_part in enumerate(path_parts):
            if path_part in self._dirs_slugs:
                url_parts[position] = self._dirs_slugs[path_part]

        # Replace last URL part with current file slug if exists
        if slug is not None and self.config.slug.enabled:
            url_parts[-1] = slug

        # Recreate file params based on URL with replaced parts
        page.file.url = f"{'/'.join(url_parts)}/"
        url_parts.append(page.file.dest_uri.split("/")[-1])
        page.file.dest_uri = "/".join(url_parts)
        page.file.abs_dest_path = str(Path(config.site_dir) / page.file.dest_uri)
        page._set_canonical_url(base=config.site_url)

        # Modify page update date
        # TODO: move date format to config
        # TODO: warn on missing in config
        update_date: datetime = page.meta.get(
            "update", page.meta.get("date", datetime.strptime(page.update_date, "%Y-%m-%d"))
        )
        page.update_date = update_date.strftime("%Y-%m-%d")
