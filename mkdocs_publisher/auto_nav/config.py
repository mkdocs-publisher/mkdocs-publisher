from mkdocs.config import config_options as option
from mkdocs.config.base import Config


class AutoNavPluginConfig(Config):
    skip_dir = option.ListOfPaths(default=[])
    meta_file_name = option.Type(str, default="README.md")
    sort_prefix_delimiter = option.Type(str, default="_")
    remove_sort_prefix_from_slug = option.Type(bool, default=True)
