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

import importlib.resources
import logging
from dataclasses import fields
from pathlib import Path
from typing import cast

import yaml

from mkdocs_publisher.blog import lang as lang_path
from mkdocs_publisher.blog.config import BlogPluginConfig
from mkdocs_publisher.blog.structures import Translation

log = logging.getLogger("mkdocs.publisher.blog.translate")


class Translate:
    def __init__(self, config: BlogPluginConfig):
        self._config: BlogPluginConfig = config
        self._translation: Translation = cast(Translation, None)

        self._read_lang()

    def _read_lang(self):
        lang_yaml_oath = Path(str(importlib.resources.files(lang_path).joinpath(f"{self._config.lang}.yaml")))
        if not lang_yaml_oath.exists():
            log.warning(
                f"There is no translation for '{self._config.lang}' language, "
                f"so default language ('{BlogPluginConfig.lang.default}') will be used"
            )
            lang_yaml_oath = str(importlib.resources.files(lang_path).joinpath(f"{BlogPluginConfig.lang.default}.yaml"))
        with open(lang_yaml_oath) as lang_yaml:
            translation_yaml_data = yaml.safe_load(lang_yaml)
        translation_keys = [f.name for f in fields(Translation)]
        translation_data = {k: v for k, v in translation_yaml_data.items() if k in translation_keys}
        # Inject overrides from mkdocs.yml config
        for key in translation_keys:
            value = self._config.translation.get(key, None)
            if value is not None:
                translation_data[key] = value
        self._translation = Translation(**translation_data)

    @property
    def translation(self) -> Translation:
        return self._translation
