# MIT License
#
# Copyright (c) 2024 Maciej 'maQ' Kusz <maciej.kusz@gmail.com>
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
from collections.abc import Generator
from pathlib import Path
from typing import Any
from typing import Optional

from mkdocs.config.defaults import MkDocsConfig
from mkdocs.structure.nav import Link
from mkdocs.structure.nav import Section
from mkdocs.structure.pages import Page

from mkdocs_publisher._shared.meta_files import MetaFile
from mkdocs_publisher._shared.meta_files import MetaFiles

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

    def _meta_files_gen(self) -> Generator[MetaFile, Any, None]:
        for meta_file in self._meta_files.values():
            meta_file: MetaFile
            if not meta_file.is_draft and not meta_file.is_hidden:
                yield meta_file

    def _build_nav(self, meta_file_gen, current_dir: Path) -> tuple[list, Optional[MetaFile]]:
        nav = []
        while True:
            # Iterate over meta links until last one
            try:
                meta_file: MetaFile = next(meta_file_gen)
            except StopIteration:
                break

            if meta_file.is_dir:
                current_meta_file = meta_file
                while current_meta_file is not None:
                    if current_meta_file.abs_path.is_relative_to(current_dir):
                        # Process current meta file that is relative to the current level directory
                        child_nav, child_meta_file = self._build_nav(
                            meta_file_gen=meta_file_gen, current_dir=current_meta_file.abs_path
                        )

                        if current_meta_file.path == self._blog_dir:
                            # Blog build its own navigation, so just preserve entry
                            nav.append({str(current_meta_file.path): str(current_meta_file.path)})
                        elif child_nav:
                            # Add an overview file
                            if current_meta_file.is_overview:
                                overview_files: list[Path] = []
                                for overview_file in self._meta_files.meta_files:
                                    if current_meta_file.abs_path.joinpath(overview_file).exists():
                                        overview_files.append(
                                            current_meta_file.path.joinpath(overview_file)
                                        )
                                if len(overview_files) > 1:
                                    log.warning(
                                        f"To much overview files in "
                                        f'"{current_meta_file}" directory'
                                    )
                                else:
                                    child_nav = [str(overview_files[0]), *child_nav]

                            # Add sub navigation to the current level one
                            nav.append({current_meta_file.title: child_nav})

                        if child_meta_file is None:
                            # Child meta file is None, so this jump to parent nav
                            return nav, None
                        else:
                            # Child meta file is returned from child level directory
                            current_meta_file = child_meta_file
                    else:
                        # When current meta file is not relative to the current directory
                        # it means that it belongs to the parent directory, so return in
                        # to the parent nav processing
                        return nav, current_meta_file
            else:
                nav.append({meta_file.title: str(meta_file.path)})
        return nav, None

    def build_nav(self, mkdocs_config: MkDocsConfig) -> list:
        nav, _ = self._build_nav(
            meta_file_gen=self._meta_files_gen(), current_dir=Path(mkdocs_config.docs_dir)
        )

        return nav
