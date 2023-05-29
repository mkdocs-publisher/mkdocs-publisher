from mkdocs.config import config_options as option
from mkdocs.config.base import Config


class _MetaSkipConfig(Config):
    dirs = option.Type(list, default=[])
    key_name = option.Type(str, default="skip_dir")


class _MetaSlugConfig(Config):
    enabled = option.Type(bool, default=True)
    warn_on_missing = option.Type(bool, default=True)
    key_name = option.Type(str, default="slug")


class _MetaTitleConfig(Config):
    key_name = option.Type(str, default="title")


class _MetaStatusConfig(Config):
    warn_on_missing = option.Type(bool, default=True)
    key_name = option.Type(str, default="status")
    search_in_hidden = option.Type(bool, default=False)
    search_in_draft = option.Type(bool, default=False)
    default = option.Choice(choices=["draft", "hidden", "published"], default="draft")


class MetaPluginConfig(Config):
    meta_file_name = option.Type(str, default="README.md")

    skip: _MetaSkipConfig = option.SubConfig(_MetaSkipConfig)  # type: ignore
    slug: _MetaSlugConfig = option.SubConfig(_MetaSlugConfig)  # type: ignore
    status: _MetaStatusConfig = option.SubConfig(_MetaStatusConfig)  # type: ignore
    title: _MetaTitleConfig = option.SubConfig(_MetaTitleConfig)  # type: ignore
