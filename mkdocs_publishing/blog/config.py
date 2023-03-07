from mkdocs.config import config_options as option
from mkdocs.config.base import Config


class _BlogInTranslationConfig(Config):
    teaser_link_text = option.Optional(option.Type(str))
    blog_page_title = option.Optional(option.Type(str))
    blog_navigation_name = option.Optional(option.Type(str))
    recent_blog_posts_navigation_name = option.Optional(option.Type(str))
    archive_page_title = option.Optional(option.Type(str))
    archive_navigation_name = option.Optional(option.Type(str))
    categories_page_title = option.Optional(option.Type(str))
    categories_navigation_name = option.Optional(option.Type(str))
    tags_page_title = option.Optional(option.Type(str))
    tags_navigation_name = option.Optional(option.Type(str))
    newer_posts = option.Optional(option.Type(str))
    older_posts = option.Optional(option.Type(str))


class BlogInPluginConfig(Config):
    # General settings
    lang = option.Choice(["en", "pl"], default="en")  # TODO: auto update based on files
    teaser_marker = option.Type(str, default="<!-- more -->")
    posts_per_page = option.Type(int, default=5)

    # Directories
    temp_dir = option.Type(str, default=".temp")
    blog_dir = option.Type(str, default="blog")
    archive_subdir = option.Type(str, default="archive")
    categories_subdir = option.Type(str, default="categories")
    tags_subdir = option.Type(str, default="tags")

    # Values that are in lang files and can be overriden
    translation: _BlogInTranslationConfig = option.SubConfig(
        _BlogInTranslationConfig
    )  # type: ignore
