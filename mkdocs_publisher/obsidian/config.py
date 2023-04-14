from mkdocs.config import config_options as option
from mkdocs.config.base import Config


class _ObsidianCalloutsConfig(Config):
    enabled = option.Type(bool, default=True)
    indentation = option.Choice(["tabs", "spaces"], default="spaces")


class _ObsidianVegaConfig(Config):
    enabled = option.Type(bool, default=True)
    vega_schema = option.Type(str, default="https://vega.github.io/schema/vega/v5.json")
    vega_lite_schema = option.Type(str, default="https://vega.github.io/schema/vega-lite/v5.json")


class ObsidianPluginConfig(Config):
    wiki_links_enabled = option.Type(bool, default=True)

    callouts: _ObsidianCalloutsConfig = option.SubConfig(_ObsidianCalloutsConfig)  # type: ignore
    vega: _ObsidianVegaConfig = option.SubConfig(_ObsidianVegaConfig)  # type: ignore
