from mkdocs.config import Config
from mkdocs.config import config_options


class BlogInPluginConfig(Config):
    # General settings
    lang = config_options.Type(str, default="en")
    teaser_marker = config_options.Type(str, default="<!-- more -->")
    posts_per_page = config_options.Type(int, default=5)

    # Directories
    cache_dir = config_options.Type(str, default=".cache")
    temp_dir = config_options.Type(str, default=".temp")
    blog_dir = config_options.Type(str, default="blog")
    archive_subdir = config_options.Type(str, default="archive")
    categories_subdir = config_options.Type(str, default="categories")
    tags_subdir = config_options.Type(str, default="tags")

    # Values that are in lang files and can be override
    teaser_link_text = config_options.Optional(config_options.Type(str))
    blog_page_title = config_options.Optional(config_options.Type(str))
    blog_navigation_name = config_options.Optional(config_options.Type(str))
    recent_blog_posts_navigation_name = config_options.Optional(config_options.Type(str))
    archive_page_title = config_options.Optional(config_options.Type(str))
    archive_navigation_name = config_options.Optional(config_options.Type(str))
    categories_page_title = config_options.Optional(config_options.Type(str))
    categories_navigation_name = config_options.Optional(config_options.Type(str))
    tags_page_title = config_options.Optional(config_options.Type(str))
    tags_navigation_name = config_options.Optional(config_options.Type(str))
    newer_posts = config_options.Optional(config_options.Type(str))
    older_posts = config_options.Optional(config_options.Type(str))
