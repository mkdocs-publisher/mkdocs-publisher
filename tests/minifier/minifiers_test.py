
from mkdocs_publisher.minifier import minifiers
from mkdocs.config.defaults import MkDocsConfig
from mkdocs_publisher.minifier.plugin import MinifierPlugin

def test_JpegMinifier(mkdocs_config: MkDocsConfig, pub_minifier_plugin: MinifierPlugin):
    plugin_config = pub_minifier_plugin.config
    cached_files = {}
    jpeg_minifier = minifiers.JpegMinifier(plugin_config=plugin_config, mkdocs_config=mkdocs_config, cached_files=cached_files)
    jpeg_minifier._minify_options = plugin_config.jpeg

    assert jpeg_minifier.are_tools_installed() == True

def test_PngMinifier(mkdocs_config: MkDocsConfig, pub_minifier_plugin: MinifierPlugin):
    plugin_config = pub_minifier_plugin.config
    cached_files = {}
    png_minifier = minifiers.PngMinifier(plugin_config=plugin_config, mkdocs_config=mkdocs_config, cached_files=cached_files)
    png_minifier._minify_options = plugin_config.png

    assert png_minifier.are_tools_installed() == True