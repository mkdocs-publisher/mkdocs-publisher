from mkdocs.config import config_options as option
from mkdocs.config.base import Config


class _MinifierCssConfig(Config):
    enabled = option.Type(bool, default=True)
    postcss_path = option.Type(str, default="postcss")
    skip_minified = option.Type(bool, default=True)


class _MinifierJsConfig(Config):
    enabled = option.Type(bool, default=True)
    uglifyjs_path = option.Type(str, default="uglifyjs")
    skip_minified = option.Type(bool, default=True)


class _MinifierHtmlConfig(Config):
    enabled = option.Type(bool, default=True)
    html_minifier_path = option.Type(str, default="html-minifier")
    case_sensitive = option.Type(bool, default=True)
    minify_css = option.Type(bool, default=True)
    minify_js = option.Type(bool, default=True)
    remove_comments = option.Type(bool, default=True)
    remove_tag_whitespace = option.Type(bool, default=True)
    collapse_whitespace = option.Type(bool, default=True)
    conservative_collapse = option.Type(bool, default=True)
    collapse_boolean_attributes = option.Type(bool, default=True)
    preserve_line_breaks = option.Type(bool, default=True)
    sort_attributes = option.Type(bool, default=True)
    sort_class_name = option.Type(bool, default=True)
    max_line_length = option.Choice(
        [str(i) for i in range(1, 4096)], default="1024"
    )  # 0 - disabled


class _MinifierSvgConfig(Config):
    enabled = option.Type(bool, default=True)
    svgo_path = option.Type(str, default="svgo")
    multipass = option.Type(bool, default=True)


class _MinifierJpgConfig(Config):
    enabled = option.Type(bool, default=True)
    djpeg_path = option.Type(str, default="djpeg")
    cjpeg_path = option.Type(str, default="cjpeg")
    jpegtran_path = option.Type(str, default="jpegtran")
    optimise = option.Type(bool, default=True)
    progressive = option.Type(bool, default=True)
    copy_meta = option.Choice(["none", "comments", "icc", "all"], default="none")
    smooth = option.Choice([str(i) for i in range(0, 101)], default="10")  # 0 - disabled
    quality = option.Choice([str(i) for i in range(0, 101)], default="85")  # 0 - disabled


class _MinifierPngConfig(Config):
    enabled = option.Type(bool, default=True)
    pngquant_enabled = option.Type(bool, default=True)
    pngquant_path = option.Type(str, default="pngquant")
    pngquant_speed = option.Choice([str(i) for i in range(1, 12)], default="1")
    pngquant_quality = option.Choice([str(i) for i in range(0, 101)], default="95")  # 0 - disabled
    oxipng_enabled = option.Type(bool, default=True)
    oxipng_path = option.Type(str, default="oxipng")
    oxipng_max_compression = option.Type(bool, default=True)
    strip = option.Type(bool, default=True)


class MinifierConfig(Config):
    cache_dir = option.Type(str, default=".cache")
    cache_file = option.Type(str, default=".cached_files_list.yml")
    threads = option.Type(int, default=0)  # 0 - default (read from system)

    js: _MinifierJsConfig = option.SubConfig(_MinifierJsConfig)  # type: ignore
    css: _MinifierCssConfig = option.SubConfig(_MinifierCssConfig)  # type: ignore
    jpg: _MinifierJpgConfig = option.SubConfig(_MinifierJpgConfig)  # type: ignore
    png: _MinifierPngConfig = option.SubConfig(_MinifierPngConfig)  # type: ignore
    svg: _MinifierSvgConfig = option.SubConfig(_MinifierSvgConfig)  # type: ignore
    html: _MinifierHtmlConfig = option.SubConfig(_MinifierHtmlConfig)  # type: ignore
