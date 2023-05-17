from mkdocs.config import config_options as option
from mkdocs.config.base import Config


class _ObsidianBacklinksConfig(Config):
    enabled = option.Type(bool, default=True)


class _ObsidianCalloutsConfig(Config):
    enabled = option.Type(bool, default=True)
    indentation = option.Choice(["tabs", "spaces"], default="spaces")


class _ObsidianVegaConfig(Config):
    enabled = option.Type(bool, default=True)
    vega_schema = option.Type(str, default="https://vega.github.io/schema/vega/v5.json")
    vega_lite_schema = option.Type(str, default="https://vega.github.io/schema/vega-lite/v5.json")


class _ObsidianLinksConfig(Config):
    wikilinks_enabled = option.Type(bool, default=True)
    img_lazy_loading = option.Type(bool, default=True)


class ObsidianPluginConfig(Config):
    obsidian_dir = option.Type(str, default=".obsidian")
    templates_dir = option.Type(str, default="_templates")

    backlinks: _ObsidianBacklinksConfig = option.SubConfig(_ObsidianBacklinksConfig)  # type: ignore
    callouts: _ObsidianCalloutsConfig = option.SubConfig(_ObsidianCalloutsConfig)  # type: ignore
    vega: _ObsidianVegaConfig = option.SubConfig(_ObsidianVegaConfig)  # type: ignore
    links: _ObsidianLinksConfig = option.SubConfig(_ObsidianLinksConfig)  # type: ignore
