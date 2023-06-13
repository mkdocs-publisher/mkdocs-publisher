from mkdocs.config import config_options as option
from mkdocs.config.base import Config


class _BlogTranslationConfig(Config):
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


class _BlogCommentsConfig(Config):
    enabled = option.Type(bool, default=False)
    key_name = option.Type(str, default="comments")


class BlogPluginConfig(Config):
    # General settings
    lang = option.Choice(["en", "pl"], default="en")  # TODO: auto update based on files
    teaser_marker = option.Type(str, default="<!-- more -->")
    searchable_non_posts = option.Type(bool, default=False)
    posts_per_page = option.Type(int, default=5)
    slug = option.Type(str, default="blog")

    # Directories
    temp_dir = option.Type(str, default=".temp")
    blog_dir = option.Type(str, default="blog")
    archive_subdir = option.Type(str, default="archive")
    categories_subdir = option.Type(str, default="categories")
    tags_subdir = option.Type(str, default="tags")

    comments: _BlogCommentsConfig = option.SubConfig(_BlogCommentsConfig)  # type: ignore
    # Values that are in lang files and can be overriden
    translation: _BlogTranslationConfig = option.SubConfig(_BlogTranslationConfig)  # type: ignore
