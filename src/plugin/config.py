from mkdocs.config import Config
from mkdocs.config import config_options


class BlogInPluginConfig(Config):
    posts_dir = config_options.Type(str, default="blog")
    index_name = config_options.Type(str, default="Blog")

    teaser_marker = config_options.Type(str, default="<!-- more -->")
    teaser_link_text = config_options.Type(str, default="Read more")

    archive_dir = config_options.Type(str, default="archive")
    archive_name = config_options.Type(str, default="Archive")

    categories_dir = config_options.Type(str, default="categories")
    categories_name = config_options.Type(str, default="Categories")

    tags_dir = config_options.Type(str, default="tags")
    tags_name = config_options.Type(str, default="Tags")

    posts_per_page = config_options.Type(int, default=5)
