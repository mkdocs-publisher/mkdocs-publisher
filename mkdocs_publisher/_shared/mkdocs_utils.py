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

import logging
from typing import cast

from mkdocs.config.defaults import MkDocsConfig

log = logging.getLogger("mkdocs.plugins.publisher._shared.mkdosc_utils")


def get_plugin_config(mkdocs_config: MkDocsConfig, plugin_name: str) -> dict:
    plugins = mkdocs_config.plugins
    if isinstance(plugins, list):
        for plugin in plugins:
            if isinstance(plugin, dict) and list(plugin.keys())[0] == plugin_name:
                return plugin[list(plugin.keys())[0]]
            elif isinstance(plugin, str) and plugin == plugin_name:
                return {}
        raise SystemError("Break")
    else:
        return mkdocs_config.plugins[plugin_name].config


def get_mkdocs_config() -> MkDocsConfig:
    config = MkDocsConfig()
    with open("mkdocs.yml", mode="r") as mkdocs_yml:
        config.load_file(mkdocs_yml)
    return cast(MkDocsConfig, config)
