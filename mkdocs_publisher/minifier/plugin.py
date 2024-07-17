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
from multiprocessing import cpu_count
from pathlib import Path
from typing import Literal
from typing import cast

import yaml
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.plugins import BasePlugin
from mkdocs.plugins import event_priority

from mkdocs_publisher.minifier import minifiers
from mkdocs_publisher.minifier.base import CachedFile
from mkdocs_publisher.minifier.config import MinifierConfig

log = logging.getLogger("mkdocs.publisher.minifier.plugin")


class MinifierPlugin(BasePlugin[MinifierConfig]):
    def __init__(self):
        self._on_serve: bool = False

    def on_startup(self, *, command: Literal["build", "gh-deploy", "serve"], dirty: bool) -> None:
        if command == "serve":
            self._on_serve = True

    @event_priority(-100)  # Run after all other plugins
    def on_post_build(self, *, config: MkDocsConfig) -> None:
        Path(self.config.cache_dir).mkdir(exist_ok=True)

        # TODO: Add path to tools checker
        cached_files: dict[str, CachedFile] = {}

        if self.config.threads == 0:
            self.config.threads = int(cpu_count())
        if self.config.threads < 1:
            log.info('Number of "threads" cannot be smaller than 1 (changing to minimal 1)')
            self.config.threads = 1
        log.info(f"Threads used for minifiers: {self.config.threads}")

        cached_files_list: Path = Path(self.config.cache_dir) / self.config.cache_file
        if cached_files_list.exists():
            try:
                with open(cached_files_list) as yaml_file:
                    cached_files = yaml.safe_load(yaml_file)
                    for file_path, cached_file in cached_files.items():
                        cached_files[file_path] = CachedFile(**cast(dict, cached_file))
            except (yaml.YAMLError, AttributeError) as e:
                log.warning(f"File '{cached_files_list}' corrupted. Rebuilding cache.")
                log.debug(e)

        if self.config.png.enabled and ((not self._on_serve) or (self._on_serve and self.config.png.enabled_on_serve)):
            minifiers.PngMinifier(plugin_config=self.config, mkdocs_config=config, cached_files=cached_files)()

        if self.config.jpeg.enabled and (
            (not self._on_serve) or (self._on_serve and self.config.jpeg.enabled_on_serve)
        ):
            minifiers.JpegMinifier(plugin_config=self.config, mkdocs_config=config, cached_files=cached_files)()

        if self.config.svg.enabled and ((not self._on_serve) or (self._on_serve and self.config.svg.enabled_on_serve)):
            minifiers.SvgMinifier(plugin_config=self.config, mkdocs_config=config, cached_files=cached_files)()

        if self.config.html.enabled and (
            (not self._on_serve) or (self._on_serve and self.config.html.enabled_on_serve)
        ):
            minifiers.HtmlMinifier(plugin_config=self.config, mkdocs_config=config, cached_files=cached_files)()

        if self.config.css.enabled and ((not self._on_serve) or (self._on_serve and self.config.css.enabled_on_serve)):
            minifiers.CssMinifier(plugin_config=self.config, mkdocs_config=config, cached_files=cached_files)()

        if self.config.js.enabled and ((not self._on_serve) or (self._on_serve and self.config.js.enabled_on_serve)):
            minifiers.JsMinifier(plugin_config=self.config, mkdocs_config=config, cached_files=cached_files)()

        cached_files_for_yaml = {}
        for file_name, cached_file in cached_files.items():
            # TODO: Cleanup yaml from unused/deleted files and delete those that are unused
            cached_file = {k: str(v) for k, v in cached_file.as_dict.items()}
            cached_files_for_yaml[file_name] = cached_file

        with open(cached_files_list, "w") as yaml_file:
            yaml.safe_dump(cached_files_for_yaml, yaml_file)
