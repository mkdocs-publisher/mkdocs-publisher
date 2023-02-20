import importlib.resources
import logging
from dataclasses import fields
from typing import Optional
from typing import cast

import yaml

from src.plugin import lang as lang_resources
from src.plugin.config import BlogInPluginConfig
from src.plugin.structures import Translation

log = logging.getLogger("mkdocs.plugins.blog-in")


class Translate:
    def __init__(self, config: BlogInPluginConfig):
        self._config: BlogInPluginConfig = config
        self._lang: str = self._config.lang
        self._translation: Optional[Translation] = None

        self._read_lang()

    def _read_lang(self):
        try:
            lang_yaml = importlib.resources.read_text(lang_resources, f"{self._config.lang}.yaml")
        except FileNotFoundError:
            log.warning(
                f"There is no translation for '{self._config.lang}' language, "
                f"so default language ('en') will be used"
            )
            # TODO: print list of existing translations
            lang_yaml = importlib.resources.read_text(
                lang_resources, f"{self._config.lang.default}.yaml"  # type: ignore
            )
        translation_yaml_data = yaml.safe_load(lang_yaml)
        translation_keys = [f.name for f in fields(Translation)]
        translation_data = {
            k: v for k, v in translation_yaml_data.items() if k in translation_keys
        }
        # Inject overrides from mkdocs.yml config
        for key in translation_keys:
            value = self._config.get(key, None)
            if value is not None:
                translation_data[key] = value
        self._translation = Translation(**translation_data)

    @property
    def translation(self) -> Translation:
        return cast(self._translation, Translation)  # type: ignore
