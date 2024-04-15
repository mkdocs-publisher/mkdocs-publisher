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
from enum import Enum
from typing import Any
from typing import Optional
from typing import Union
from typing import cast

from mkdocs.config.base import Config
from mkdocs.config.defaults import MkDocsConfig

log = logging.getLogger("mkdocs.plugins.publisher._shared.mkdocs_utils")


class ConfigChoiceEnum(Enum):
    def __eq__(self, other) -> bool:
        if isinstance(other, bool) and self.is_bool:
            return self._str_to_bool(self.name) is other
        return self.name.lower() == str(other).lower()

    def __hash__(self):
        return super().__hash__()

    @staticmethod
    def _str_to_bool(text) -> bool:
        if text.lower() == "true":
            return True
        elif text.lower() == "false":
            return False
        raise ValueError(f"'{text}' cannot be converted into bool value")

    @classmethod
    def _get_enums(cls, enums: list) -> list:
        enums_list = []
        for enum in enums:
            if enum.is_bool:
                enums_list.extend([enum.name, cls._str_to_bool(enum.name)])
            else:
                enums_list.append(enum.name)
        return enums_list

    @property
    def name(self) -> str:
        return ".".join(str(self).split(".")[1:]).lower()

    @property
    def is_bool(self) -> bool:
        return self.value[2]

    @classmethod
    def default(cls) -> Optional[str]:
        defaults = [f.name for f in cls if f.value[1]]
        if len(defaults) == 0:
            return None
        elif len(defaults) > 1:
            raise ValueError(f"Multiple defaults specified: {defaults}")
        return defaults[0]

    @classmethod
    def choices(cls) -> list:
        return cls._get_enums(enums=cast(list, cls))


def get_plugin_config(
    mkdocs_config: MkDocsConfig, plugin_name: str
) -> Union[None, dict[str, Any], Config]:
    plugins = mkdocs_config.plugins
    if isinstance(plugins, list):
        for plugin in plugins:
            if isinstance(plugin, dict) and list(plugin.keys())[0] == plugin_name:
                return plugin[list(plugin.keys())[0]]
            elif isinstance(plugin, str) and plugin == plugin_name:
                return {}
        raise SystemError("Break")
    else:
        if plugin_name in mkdocs_config.plugins:
            return mkdocs_config.plugins[plugin_name].config
        else:
            return None


def get_mkdocs_config() -> MkDocsConfig:
    config = MkDocsConfig()
    with open("mkdocs.yml") as mkdocs_yml:
        config.load_file(mkdocs_yml)
    return cast(MkDocsConfig, config)
