import importlib.resources
from pathlib import Path

from mkdocs.config.defaults import MkDocsConfig
from mkdocs.structure.files import File
from mkdocs.structure.files import Files

from mkdocs_publisher._extra import assets

# noinspection PyProtectedMember
from mkdocs_publisher._extra.assets import stylesheets
from mkdocs_publisher._extra.assets import templates


def add_extra_css(stylesheet_file_name: str, config: MkDocsConfig, files: Files):
    """Add CSS file from mkdocs_publisher._extra to mkdosc.yml config file"""

    resource_file_path = Path(
        str(importlib.resources.files(stylesheets).joinpath(stylesheet_file_name))
    )
    assets_path = Path(str(importlib.resources.files(assets)))
    css_file_path = str(resource_file_path.relative_to(assets_path.parent))

    files.append(
        File(
            path=css_file_path,
            src_dir=str(assets_path.parent),
            dest_dir=str(config.site_dir),
            use_directory_urls=config.use_directory_urls,
        )
    )
    config.extra_css.append(css_file_path)  # type: ignore


def read_template_file(template_file_name: str) -> str:
    """Read and return content of template file"""
    resource_file_path = importlib.resources.files(templates).joinpath(template_file_name)
    with importlib.resources.as_file(resource_file_path) as template_file:
        return template_file.read_text(encoding="utf-8")
