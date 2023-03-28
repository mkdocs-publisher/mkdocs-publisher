import logging
from typing import Optional

from mkdocs_publisher import _utils
from mkdocs_publisher.minifier.base import BaseMinifier
from mkdocs_publisher.minifier.base import CachedFile

log = logging.getLogger("mkdocs.plugins.publisher.minifier")


class PngMinifier(BaseMinifier):
    extensions = [".png"]

    def minifier(self, cached_file: CachedFile) -> Optional[CachedFile]:
        minify_options = self._plugin_config.png
        try:
            input_file = self._mkdocs_config.site_dir / cached_file.original_file_path
            output_file = self._plugin_config.cache_dir / cached_file.cached_file_name

            if minify_options.pngquant_enabled:
                pngquant_cmd = [
                    minify_options.pngquant_path,
                    "--force",
                    "--strip" if minify_options.strip else None,
                    "--quality" if int(minify_options.pngquant_quality) > 0 else None,
                    minify_options.pngquant_quality
                    if int(minify_options.pngquant_quality) > 0
                    else None,
                    "--speed",
                    minify_options.pngquant_speed,
                    "--output",
                    str(output_file),
                    str(input_file),
                ]
                if _utils.run_subprocess(cmd=pngquant_cmd) != 0:
                    output_file.unlink(missing_ok=True)
                    return None

            if minify_options.oxipng_enabled:
                oxipng_cmd = [
                    minify_options.oxipng_path,
                    "--quiet",
                    "--force",
                    "--strip" if minify_options.strip else None,
                    "all" if minify_options.strip else None,
                    "--zopfli" if minify_options.oxipng_max_compression else None,
                    "--out" if not minify_options.pngquant_enabled else None,
                    str(output_file) if not minify_options.pngquant_enabled else None,
                    str(input_file) if not minify_options.pngquant_enabled else str(output_file),
                ]
                if _utils.run_subprocess(cmd=oxipng_cmd) != 0:
                    output_file.unlink(missing_ok=True)
                    return None

                return cached_file

        except FileNotFoundError as e:
            log.warning(e)

        return None


class JpgMinifier(BaseMinifier):
    extensions = [".jpg", ".jpeg"]

    def minifier(self, cached_file: CachedFile) -> Optional[CachedFile]:
        minify_options = self._plugin_config.jpg
        try:
            input_file = self._mkdocs_config.site_dir / cached_file.original_file_path
            output_file = self._plugin_config.cache_dir / cached_file.cached_file_name

            djpg_cmd = [
                minify_options.djpeg_path,
                "-targa",
                "-outfile",
                str(output_file.with_suffix(".tga")),
                str(input_file),
            ]
            if _utils.run_subprocess(cmd=djpg_cmd) != 0:
                output_file.with_suffix(".tga").unlink(missing_ok=True)
                return None

            cjpg_cmd = [
                minify_options.cjpeg_path,
                "-targa",
                "-smooth" if int(minify_options.smooth) > 0 else None,
                minify_options.smooth if int(minify_options.smooth) > 0 else None,
                "-quality" if int(minify_options.quality) > 0 else None,
                minify_options.quality if int(minify_options.quality) > 0 else None,
                "-outfile",
                str(output_file.with_suffix(".jpg_")),
                str(output_file.with_suffix(".tga")),
            ]
            if _utils.run_subprocess(cmd=cjpg_cmd) != 0:
                output_file.with_suffix(".jpg_").unlink(missing_ok=True)
                return None
            output_file.with_suffix(".tga").unlink(missing_ok=True)

            jpegtran_cmd = [
                minify_options.jpegtran_path,
                "-copy",
                minify_options.copy_meta,
                "-progressive" if minify_options.progressive else None,
                "-optimise" if minify_options.optimise else None,
                "-outfile",
                str(output_file),
                str(output_file.with_suffix(".jpg_")),
            ]
            if _utils.run_subprocess(cmd=jpegtran_cmd) != 0:
                output_file.unlink(missing_ok=True)
                return None
            output_file.with_suffix(".jpg_").unlink(missing_ok=True)

            return cached_file

        except FileNotFoundError as e:
            log.warning(e)

        return None


class SvgMinifier(BaseMinifier):
    extensions = [".svg"]

    def minifier(self, cached_file: CachedFile) -> Optional[CachedFile]:
        minify_options = self._plugin_config.svg
        try:
            input_file = self._mkdocs_config.site_dir / cached_file.original_file_path
            output_file = self._plugin_config.cache_dir / cached_file.cached_file_name

            svgo_cmd = [
                minify_options.svgo_path,
                "--multipass" if minify_options.multipass else None,
                "--quiet",
                "--output",
                str(output_file),
                "--input",
                str(input_file),
            ]
            if _utils.run_subprocess(cmd=svgo_cmd) != 0:
                output_file.unlink(missing_ok=True)
                return None

            return cached_file

        except FileNotFoundError as e:
            log.warning(e)

        return None


class HtmlMinifier(BaseMinifier):
    extensions = [".htm", ".html"]

    def minifier(self, cached_file: CachedFile) -> Optional[CachedFile]:
        minify_options = self._plugin_config.html
        try:
            input_file = self._mkdocs_config.site_dir / cached_file.original_file_path
            output_file = self._plugin_config.cache_dir / cached_file.cached_file_name

            html_minifier_cmd = [
                minify_options.html_minifier_path,
                "--case-sensitive" if minify_options.case_sensitive else None,
                "--minify-css" if minify_options.minify_css else None,
                "--minify-js" if minify_options.minify_js else None,
                "--remove-comments" if minify_options.remove_comments else None,
                "--remove-tag-whitespace" if minify_options.remove_tag_whitespace else None,
                "--collapse-whitespace" if minify_options.collapse_whitespace else None,
                "--conservative-collapse" if minify_options.conservative_collapse else None,
                "--collapse-boolean-attributes"
                if minify_options.collapse_boolean_attributes
                else None,
                "--preserve-line-breaks" if minify_options.preserve_line_breaks else None,
                "--max-line-length" if int(minify_options.max_line_length) > 0 else None,
                minify_options.max_line_length
                if int(minify_options.max_line_length) > 0
                else None,
                "--sort-attributes" if minify_options.sort_attributes else None,
                "--sort-class-name" if minify_options.sort_class_name else None,
                "--output",
                str(output_file),
                str(input_file),
            ]
            if _utils.run_subprocess(cmd=html_minifier_cmd) != 0:
                output_file.unlink(missing_ok=True)
                return None

            return cached_file

        except FileNotFoundError as e:
            log.warning(e)

        return None


class CssMinifier(BaseMinifier):
    extensions = [".css"]

    def minifier(self, cached_file: CachedFile) -> Optional[CachedFile]:
        minify_options = self._plugin_config.css
        try:
            input_file = self._mkdocs_config.site_dir / cached_file.original_file_path
            output_file = self._plugin_config.cache_dir / cached_file.cached_file_name

            if ".min" in input_file.suffixes and minify_options.skip_minified:
                return None
            css_minifier_cmd = [
                minify_options.postcss_path,
                "--no-map",
                "--use",
                "cssnano",
                "postcss-svgo",
                "--output",
                str(output_file),
                str(input_file),
            ]
            if _utils.run_subprocess(cmd=css_minifier_cmd) != 0:
                output_file.unlink(missing_ok=True)
                return None

            return cached_file

        except FileNotFoundError as e:
            log.warning(e)

        return None


class JsMinifier(BaseMinifier):
    extensions = [".js"]

    def minifier(self, cached_file: CachedFile) -> Optional[CachedFile]:
        minify_options = self._plugin_config.js
        try:
            input_file = self._mkdocs_config.site_dir / cached_file.original_file_path
            output_file = self._plugin_config.cache_dir / cached_file.cached_file_name

            if ".min" in input_file.suffixes and minify_options.skip_minified:
                return None
            js_minifier_cmd = [
                minify_options.uglifyjs_path,
                "--compress",
                "--webkit",
                "--output",
                str(output_file),
                str(input_file),
            ]
            if _utils.run_subprocess(cmd=js_minifier_cmd) != 0:
                output_file.unlink(missing_ok=True)
                return None

            return cached_file

        except FileNotFoundError as e:
            log.warning(e)

        return None
