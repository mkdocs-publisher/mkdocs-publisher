from mkdocs.config import config_options as option
from mkdocs.config.base import Config


class _SocialOpenGraphConfig(Config):
    enabled = option.Type(bool, default=True)
    locale = option.Type(str, default="en_us")


class _SocialTwitterConfig(Config):
    enabled = option.Type(bool, default=True)
    website = option.Type(str, default="")
    author = option.Type(str, default="")


class _SocialMetaKeysConfig(Config):
    title_key = option.Type(str, default="title")
    description_key = option.Type(str, default="description")
    image_key = option.Type(str, default="image")


class SocialConfig(Config):
    twitter: _SocialTwitterConfig = option.SubConfig(_SocialTwitterConfig)  # type: ignore
    og: _SocialOpenGraphConfig = option.SubConfig(_SocialOpenGraphConfig)  # type: ignore
    meta_keys: _SocialMetaKeysConfig = option.SubConfig(_SocialMetaKeysConfig)  # type: ignore
