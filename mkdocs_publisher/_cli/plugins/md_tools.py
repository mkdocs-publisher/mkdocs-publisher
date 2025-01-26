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

import json
import logging
from pathlib import Path

import click
import yaml
from mkdocs.utils import meta as meta_parser

from mkdocs_publisher._shared import mkdocs_utils
from mkdocs_publisher.obsidian.plugin import ObsidianPlugin

log = logging.getLogger("mkdocs.publisher.cli.md_tools")


@click.group
def app():
    """Markdown tools."""
    pass


@app.command()
def key_rename():
    mkdocs_config = mkdocs_utils.get_mkdocs_config()
    obsidian_plugin = ObsidianPlugin()
    obsidian_plugin.load_config(options={"plugins": mkdocs_config.plugins})

    obsidian_config_dir = Path(mkdocs_config.docs_dir) / obsidian_plugin.config.obsidian_dir
    linter_config_file = Path(obsidian_config_dir) / "plugins/obsidian-linter/data.json"

    key_order_list = []
    if linter_config_file.is_file():
        with linter_config_file.open("r") as linter_json:
            linter_config = json.load(linter_json)["ruleConfigs"]
            key_order_list = str(linter_config["yaml-key-sort"]["yaml-key-priority-sort-order"]).split("\n")

    # old_key_name = click.prompt("Enter old key name you want to replace", type=str)  # noqa: ERA001
    old_key_name = "visibility"
    # new_key_name = click.prompt("Enter new key name", type=str)  # noqa: ERA001
    new_key_name = "publish"

    for file_path in Path(mkdocs_config.docs_dir).glob("**/*.md"):
        output = "---\n"
        with file_path.open(encoding="utf-8-sig", errors="strict", mode="r+") as md_file:
            content, post_meta = meta_parser.get_data(md_file.read())
            for key in key_order_list:
                if key in post_meta and key in post_meta:
                    output = f"{output}{yaml.safe_dump({key: post_meta[key]}, indent=2)}"
                    post_meta.pop(key, None)
                elif key in [old_key_name, new_key_name] and old_key_name in post_meta:
                    yaml_text_dump = yaml.safe_dump({new_key_name: post_meta[old_key_name]}, indent=2)
                    output = f"{output}{yaml_text_dump}"
                    post_meta.pop(old_key_name, None)
            for key in post_meta:
                output = f"{output}{yaml.safe_dump({key: post_meta[key]}, indent=2)}"
            output = f"{output}---\n\n{content}"
            md_file.seek(0)
            md_file.write(output)
