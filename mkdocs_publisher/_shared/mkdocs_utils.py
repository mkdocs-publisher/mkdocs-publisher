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

import logging
import re
from functools import lru_cache
from pathlib import Path
from typing import Any
from typing import TypeVar
from typing import cast

from mkdocs.config.defaults import MkDocsConfig
from mkdocs.utils import meta as meta_parser
from mkdocs.utils import yaml

from mkdocs_publisher._shared import links
from mkdocs_publisher.blog.config import BlogPluginConfig
from mkdocs_publisher.debugger.config import DebuggerPluginConfig
from mkdocs_publisher.meta.config import MetaPluginConfig
from mkdocs_publisher.minifier.config import MinifierPluginConfig
from mkdocs_publisher.obsidian.config import ObsidianPluginConfig
from mkdocs_publisher.social.config import SocialPluginConfig

log = logging.getLogger("mkdocs.publisher._shared.mkdocs_utils")


ADMONITIONS_RE = re.compile(r"\[!\w+]")
COMMENTS_RE = re.compile(r"<!--(.*?)-->", flags=re.MULTILINE)
CODE_BLOCK_RE = re.compile(r"`{3}[^>]*`{3}", flags=re.MULTILINE)
COMMA_RE = re.compile(" ,")
ENUMERATIONS_RE = re.compile(r"[0-9#]*\.")
FOOTNOTES_RE = re.compile(r"^\[[^]]*][^(].*", flags=re.MULTILINE)
FOOTNOTES_REF_RE = re.compile(r"\[[0-9]*]")
HEADERS_ID_RE = re.compile(r"{#.*}")
HTML_RE = re.compile(r"</?[^>]*>")
NEW_LINE_RE = re.compile(r"\n")
SPACES_RE = re.compile(r" {2,}")
SPECIAL_CHARS_RE = re.compile(r"[#*`~\-_^=<>+|/:]")
TAB_RE = re.compile(r"\t")

PLUGIN_CONFIG_MAPPING = {
    BlogPluginConfig: "pub-blog",
    DebuggerPluginConfig: "pub-debugger",
    MetaPluginConfig: "pub-meta",
    MinifierPluginConfig: "pub-minifier",
    ObsidianPluginConfig: "pub-obsidian",
    SocialPluginConfig: "pub-social",
}

PluginConfigType = TypeVar(
    "PluginConfigType",
    BlogPluginConfig,
    DebuggerPluginConfig,
    MetaPluginConfig,
    MinifierPluginConfig,
    ObsidianPluginConfig,
    SocialPluginConfig,
)


@lru_cache
def get_mkdocs_config() -> MkDocsConfig:
    mkdocs_config = MkDocsConfig()
    with Path("mkdocs.yml").open() as mkdocs_yaml_file:
        mkdocs_config_dict = yaml.yaml_load(mkdocs_yaml_file)
        mkdocs_config.set_defaults()
        mkdocs_config.load_dict(patch=mkdocs_config_dict)
    return cast(MkDocsConfig, mkdocs_config)


def get_plugin_config(
    plugin_config_type: PluginConfigType,
    mkdocs_config: MkDocsConfig,
) -> PluginConfigType | list[PluginConfigType] | None:
    plugin_config: PluginConfigType | None = None
    plugin_name = PLUGIN_CONFIG_MAPPING[plugin_config_type]  # type: ignore[reportArgumentType]

    if isinstance(mkdocs_config.plugins, list):
        plugin_config_dict = {}

        for plugin in mkdocs_config.plugins:
            if isinstance(plugin, dict) and next(iter(plugin.keys())) == plugin_name:
                plugin_config_dict = plugin[next(iter(plugin.keys()))]
            elif isinstance(plugin, str) and plugin == plugin_name:
                plugin_config_dict = {}

        if plugin_config_dict:
            plugin_config = cast(
                PluginConfigType,
                plugin_config_type(config_file_path=mkdocs_config.config_file_path),  # type: ignore[reportCallIssue]
            )
            plugin_config.load_dict(patch=plugin_config_dict)
            plugin_config.validate()
            return plugin_config
    elif isinstance(mkdocs_config.plugins, dict):
        if plugin_name in mkdocs_config.plugins:
            return cast(PluginConfigType, mkdocs_config.plugins[plugin_name].config)
    return None


@lru_cache
def read_md_file(md_file_path: Path) -> tuple[str, dict[str, Any]]:  # pragma: no cover
    with md_file_path.open(encoding="utf-8-sig", errors="strict") as md_file:
        # Add empty line at the end of file and read all data
        return meta_parser.get_data(f"{md_file.read()}\n")


def _md_any_link_to_text(match: re.Match) -> str:
    return f'{match.groupdict()["text"]} '


def count_words(content: str):
    """Count words in markdown content.

    Based on: https://github.com/gandreadis/markdown-word-count
    """
    content = re.sub(TAB_RE, "    ", content)
    content = re.sub(NEW_LINE_RE, " ", content)
    content = re.sub(SPACES_RE, "    ", content)
    content = re.sub(COMMENTS_RE, "", content)
    content = re.sub(FOOTNOTES_RE, "", content)
    content = re.sub(FOOTNOTES_REF_RE, "", content)
    content = re.sub(CODE_BLOCK_RE, "", content)
    content = re.sub(HEADERS_ID_RE, "", content)
    content = re.sub(HTML_RE, "", content)
    content = re.sub(SPECIAL_CHARS_RE, "", content)
    content = re.sub(ENUMERATIONS_RE, "", content)
    content = re.sub(ADMONITIONS_RE, "", content)
    content = re.sub(SPACES_RE, " ", content)
    content = re.sub(links.MD_ANY_LINK_RE, _md_any_link_to_text, content)
    content = re.sub(COMMA_RE, ",", content)

    return len(content.split())
