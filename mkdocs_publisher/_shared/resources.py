# MIT License
#
# Copyright (c) 2023 Maciej 'maQ' Kusz <maciej.kusz@gmail.com>
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

import importlib.resources
import logging
from pathlib import Path

from mkdocs.config.defaults import MkDocsConfig
from mkdocs.structure.files import File
from mkdocs.structure.files import Files

from mkdocs_publisher._extra import assets

# noinspection PyProtectedMember
from mkdocs_publisher._extra.assets import stylesheets
from mkdocs_publisher._extra.assets import templates

log = logging.getLogger("mkdocs.plugins.publisher._shared.resources")


def _add_extra_file(
    resource_file_path: Path,
    config: MkDocsConfig,
    files: Files,
):
    assets_path = Path(str(importlib.resources.files(assets)))
    extra_file_path = str(resource_file_path.relative_to(assets_path.parent))
    if resource_file_path.exists():
        files.append(
            File(
                path=extra_file_path,
                src_dir=str(assets_path.parent),
                dest_dir=str(config.site_dir),
                use_directory_urls=config.use_directory_urls,
            )
        )
        config.extra_css.append(extra_file_path)
        log.debug(f"Extra file added: {extra_file_path}")
    else:
        log.error(f"Extra file doesn't exists: {extra_file_path}")


def add_extra_css(
    stylesheet_file_name: str, config: MkDocsConfig, files: Files, add_map: bool = True
):
    """Add CSS file from mkdocs_publisher._extra to mkdocs.yml config file"""

    css_file_path = Path(
        str(importlib.resources.files(stylesheets).joinpath(stylesheet_file_name))
    )
    _add_extra_file(resource_file_path=css_file_path, config=config, files=files)

    if add_map:
        css_map_file_path = Path(
            str(importlib.resources.files(stylesheets).joinpath(f"{stylesheet_file_name}.map"))
        )
        _add_extra_file(resource_file_path=css_map_file_path, config=config, files=files)


def read_template_file(template_file_name: str) -> str:
    """Read and return content of template file"""
    resource_file_path = importlib.resources.files(templates).joinpath(template_file_name)
    with importlib.resources.as_file(resource_file_path) as template_file:
        return template_file.read_text(encoding="utf-8")
