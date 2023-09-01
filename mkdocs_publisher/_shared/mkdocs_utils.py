from typing import Optional

from mkdocs.config.base import Config
from mkdocs.config.defaults import MkDocsConfig


def get_plugin_config(mkdocs_config: MkDocsConfig, plugin_name: str) -> Optional[Config]:
    try:
        return mkdocs_config.plugins[plugin_name].config
    except KeyError:
        return None
