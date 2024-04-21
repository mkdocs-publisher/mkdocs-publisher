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
from pathlib import Path
from typing import Optional

from mkdocs.config.defaults import MkDocsConfig
from mkdocs.structure.nav import Link
from mkdocs.structure.nav import Section
from mkdocs.structure.pages import Page

from mkdocs_publisher.meta.meta_files import MetaFile
from mkdocs_publisher.meta.meta_files import MetaFiles

log = logging.getLogger("mkdocs.plugins.publisher.meta.nav")


class MetaNav:
    def __init__(self, meta_files: MetaFiles, blog_dir: Optional[Path] = None):
        self._meta_files: MetaFiles = meta_files
        self._blog_dir: Optional[Path] = blog_dir

    def nav_cleanup(self, items, removal_list: list[str]) -> list:
        nav = []
        for item in items:
            if isinstance(item, Section):
                item.children = self.nav_cleanup(items=item.children, removal_list=removal_list)
                # If section is empty, skip it
                if len(item.children) > 0:
                    nav.append(item)
            elif (isinstance(item, Page) and str(item.file.src_path) not in removal_list) or (
                isinstance(item, Link) and item.title not in removal_list
            ):
                nav.append(item)
        return nav

    def _build_nav(self, meta_files_gen, current_dir: Path) -> tuple[list, Optional[MetaFile]]:
        nav = []
        meta_file: Optional[MetaFile] = None
        while True:
            if meta_file is None:
                try:
                    meta_file = next(meta_files_gen)
                except StopIteration:
                    break
            # Iterate over meta links until last one
            if meta_file.is_dir and meta_file.abs_path.is_relative_to(current_dir):
                overview_path: Path = meta_file.abs_path.joinpath(self._meta_files.meta_file)
                overview_nav: list[Path] = (
                    [meta_file.path.joinpath(self._meta_files.meta_file)]
                    if meta_file.is_overview and overview_path.exists()
                    else []
                )

                title = meta_file.title
                prev_path = meta_file.path
                sub_nav, meta_file = self._build_nav(
                    meta_files_gen=meta_files_gen, current_dir=meta_file.abs_path
                )
                sub_nav = [*overview_nav, *sub_nav]
                if sub_nav:
                    if prev_path == self._blog_dir:
                        nav.append({str(prev_path): str(prev_path)})
                    else:
                        nav.append({title: sub_nav})
            elif meta_file.is_dir:
                return nav, meta_file  # Jump to subdirectory
            elif (
                not meta_file.is_dir and not meta_file.is_draft and meta_file.path.suffix == ".md"
            ):
                if meta_file.abs_path.is_relative_to(current_dir):
                    nav.append({meta_file.title: str(meta_file.path)})
                    meta_file = None  # File added, skip to next
                else:
                    return nav, meta_file  # Jump to subdirectory
            else:
                meta_file = None  # File not to be processed, skip to next
        return nav, None

    def build_nav(self, mkdocs_config: MkDocsConfig) -> list:
        nav, _ = self._build_nav(
            meta_files_gen=self._meta_files.files_gen(),
            current_dir=Path(mkdocs_config.docs_dir),
        )
        return nav
