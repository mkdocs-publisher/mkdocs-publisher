import importlib
import pathlib

import click


@click.group
def app():
    """Publisher plugin for MkDocs (by Maciej 'maQ' Kusz).

    More information can be fount at: https://github.com/mkusz/mkdocs-publisher
    """
    pass


def build_app(app: click.group):  # type: ignore
    plugins_path = pathlib.Path(__file__).parent.resolve() / "plugins"
    for plugin_file_name in pathlib.Path(plugins_path).rglob("*.py"):
        plugin_name = pathlib.PurePath(plugin_file_name).stem
        plugin_module = importlib.import_module(f"mkdocs_publisher._cli.plugins.{plugin_name}")
        app.add_command(cmd=getattr(plugin_module, "app", plugin_name), name=str(plugin_name))


build_app(app=app)


if __name__ == "__main__":
    app()
