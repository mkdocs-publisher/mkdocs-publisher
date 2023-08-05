import logging
from multiprocessing import cpu_count
from pathlib import Path
from typing import Dict
from typing import cast

import yaml
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.plugins import BasePlugin
from mkdocs.plugins import event_priority

from mkdocs_publisher.minifier import minifiers
from mkdocs_publisher.minifier.base import CachedFile
from mkdocs_publisher.minifier.config import MinifierConfig

log = logging.getLogger("mkdocs.plugins.publisher.minifier.plugin")


class MinifierPlugin(BasePlugin[MinifierConfig]):
    @event_priority(-100)  # Run after all other plugins
    def on_post_build(self, *, config: MkDocsConfig) -> None:

        Path(self.config.cache_dir).mkdir(exist_ok=True)

        # TODO: Add path to tools checker
        cached_files: Dict[str, CachedFile] = {}

        if self.config.threads == 0:
            self.config.threads = int(cpu_count())
        log.info(f"Threads used for minifiers: {self.config.threads}")

        cached_files_list: Path = Path(self.config.cache_dir) / self.config.cache_file
        if cached_files_list.exists():
            try:
                with open(cached_files_list, "r") as yaml_file:
                    cached_files = yaml.safe_load(yaml_file)
                    for file_path, cached_file in cached_files.items():
                        cached_files[file_path] = CachedFile(**cast(dict, cached_file))
            except (yaml.YAMLError, AttributeError) as e:
                log.warning(f"File '{cached_files_list}' corrupted. Rebuilding cache.")
                log.debug(e)

        if self.config.png.enabled:
            minifiers.PngMinifier(
                plugin_config=self.config, mkdocs_config=config, cached_files=cached_files
            )()

        if self.config.jpg.enabled:
            minifiers.JpgMinifier(
                plugin_config=self.config, mkdocs_config=config, cached_files=cached_files
            )()

        if self.config.svg.enabled:
            minifiers.SvgMinifier(
                plugin_config=self.config, mkdocs_config=config, cached_files=cached_files
            )()

        if self.config.html.enabled:
            minifiers.HtmlMinifier(
                plugin_config=self.config, mkdocs_config=config, cached_files=cached_files
            )()

        if self.config.css.enabled:
            minifiers.CssMinifier(
                plugin_config=self.config, mkdocs_config=config, cached_files=cached_files
            )()

        if self.config.js.enabled:
            minifiers.JsMinifier(
                plugin_config=self.config, mkdocs_config=config, cached_files=cached_files
            )()

        cached_files_for_yaml = {}
        for file_name, cached_file in cached_files.items():
            # TODO: Cleanup yaml from unused/deleted files and delete those that are unused
            cached_file = {k: str(v) for k, v in cached_file.as_dict.items()}
            cached_files_for_yaml[file_name] = cached_file

        with open(cached_files_list, "w") as yaml_file:
            yaml.safe_dump(cached_files_for_yaml, yaml_file)
