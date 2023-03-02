from mkdocs.config import config_options as option
from mkdocs.config.base import Config


class _BlogInMinifySvgCongig(Config):
    enabled = option.Type(bool, default=True)
    svgo_path = option.Type(str, default="svgo")
    multipass = option.Type(bool, default=True)


class _BlogInMinifyJpgCongig(Config):
    enabled = option.Type(bool, default=True)
    djpeg_path = option.Type(str, default="djpeg")
    cjpeg_path = option.Type(str, default="cjpeg")
    jpegtran_path = option.Type(str, default="jpegtran")
    optimise = option.Type(bool, default=True)
    progressive = option.Type(bool, default=True)
    copy_meta = option.Choice(["none", "comments", "icc", "all"], default="none")
    smooth = option.Choice([str(i) for i in range(0, 101)], default="10")  # 0 - disabled
    quality = option.Choice([str(i) for i in range(0, 101)], default="85")  # 0 - disabled


class _BlogInMinifyPngConfig(Config):
    enabled = option.Type(bool, default=True)
    pngquant_enabled = option.Type(bool, default=True)
    pngquant_path = option.Type(str, default="pngquant")
    pngquant_speed = option.Choice([str(i) for i in range(1, 12)], default="1")
    oxipng_enabled = option.Type(bool, default=True)
    oxipng_path = option.Type(str, default="oxipng")
    oxipng_max_compression = option.Type(bool, default=True)
    strip = option.Type(bool, default=True)


class _BlogInMinifyConfig(Config):
    enabled = option.Type(bool, default=True)
    cache_dir = option.Type(str, default=".cache")
    cache_file = option.Type(str, default=".cached_files_list.yml")
    threads = option.Type(int, default=8)

    png: _BlogInMinifyPngConfig = option.SubConfig(_BlogInMinifyPngConfig)  # type: ignore
    jpg: _BlogInMinifyJpgCongig = option.SubConfig(_BlogInMinifyJpgCongig)  # type: ignore
    svg: _BlogInMinifySvgCongig = option.SubConfig(_BlogInMinifySvgCongig)  # type: ignore


class BlogInPluginConfig(Config):
    # General settings
    lang = option.Type(str, default="en")
    teaser_marker = option.Type(str, default="<!-- more -->")
    posts_per_page = option.Type(int, default=5)

    # Directories
    temp_dir = option.Type(str, default=".temp")
    blog_dir = option.Type(str, default="blog")
    archive_subdir = option.Type(str, default="archive")
    categories_subdir = option.Type(str, default="categories")
    tags_subdir = option.Type(str, default="tags")

    # Values that are in lang files and can be override
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

    minify: _BlogInMinifyConfig = option.SubConfig(_BlogInMinifyConfig)  # type: ignore
