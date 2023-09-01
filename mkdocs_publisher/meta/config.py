from mkdocs.config import config_options as option
from mkdocs.config.base import Config


class _MetaSlugConfig(Config):
    enabled = option.Type(bool, default=True)
    warn_on_missing = option.Type(bool, default=True)
    key_name = option.Type(str, default="slug")


class _MetaStatusConfig(Config):
    search_in_hidden = option.Type(bool, default=False)
    search_in_draft = option.Type(bool, default=False)
    file_default = option.Choice(choices=["draft", "hidden", "published"], default="draft")
    file_warn_on_missing = option.Type(bool, default=True)
    dir_default = option.Choice(choices=["draft", "hidden", "published"], default="published")
    dir_warn_on_missing = option.Type(bool, default=False)
    key_name = option.Type(str, default="status")


class _MetaTitleConfig(Config):
    key_name = option.Type(str, default="title")


class MetaPluginConfig(Config):
    dir_meta_file = option.Type(str, default="README.md")

    slug: _MetaSlugConfig = option.SubConfig(_MetaSlugConfig)  # type: ignore
    status: _MetaStatusConfig = option.SubConfig(_MetaStatusConfig)  # type: ignore
    title: _MetaTitleConfig = option.SubConfig(_MetaTitleConfig)  # type: ignore
