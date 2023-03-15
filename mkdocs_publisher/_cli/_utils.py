from pathlib import Path
from typing import cast

from mkdocs import config
from mkdocs import utils
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.plugins import BasePlugin

from blog.config import BlogPluginConfig
from blog.plugin import BlogPlugin


def mkdocs_cfg() -> MkDocsConfig:
    return config.load_config(config_file=open(Path.cwd() / "mkdocs.yml", "rb"))


def blog_in_cfg() -> BlogPluginConfig:
    plugin = BlogPlugin()

    options = {}
    yaml_file = cast(dict, utils.yaml_load(open(Path.cwd() / "mkdocs.yml", "rb")))
    for plugin in cast(list, yaml_file.get("plugins")):
        if isinstance(plugin, dict) and list(plugin.keys())[0] == "blog":
            options = list(plugin.values())[0]

    plugin: BasePlugin
    plugin.load_config(options=options, config_file_path=str(Path.cwd() / "mkdocs.yml"))

    return plugin.config
