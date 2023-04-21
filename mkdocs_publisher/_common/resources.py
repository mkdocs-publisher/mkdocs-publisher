import importlib
import importlib.resources
import importlib.util

from mkdocs.config.defaults import MkDocsConfig
from mkdocs.structure.files import File
from mkdocs.structure.files import Files

from mkdocs_publisher._extra.assets import stylesheets


def add_extra_css(stylesheet_file_name: str, config: MkDocsConfig, files: Files):
    with importlib.resources.path(
        importlib.import_module("mkdocs_publisher._extra"), "__init__.py"
    ) as extra_path:
        with importlib.resources.path(
            importlib.import_module(stylesheets.__name__), stylesheet_file_name
        ) as stylesheets_file:
            css_file_path = str(stylesheets_file.relative_to(extra_path.parent))
            files.append(
                File(
                    path=css_file_path,
                    src_dir=str(extra_path.parent),
                    dest_dir=str(config.site_dir),
                    use_directory_urls=config.use_directory_urls,
                )
            )
            config.extra_css.append(css_file_path)
