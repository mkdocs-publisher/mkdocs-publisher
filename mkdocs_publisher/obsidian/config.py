from mkdocs.config import config_options as option
from mkdocs.config.base import Config


class ObsidianPluginConfig(Config):
    enabled = option.Type(bool, default=True)
