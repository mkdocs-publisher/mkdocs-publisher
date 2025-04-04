# MIT License
#
# Copyright (c) 2023-2025 Maciej 'maQ' Kusz <maciej.kusz@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import importlib
import logging
import pathlib

import click


@click.group
@click.option("--debug", is_flag=True, default=False, help="Show debug messages")
def app(debug: bool) -> None:
    """Publisher plugin for MkDocs (by Maciej 'maQ' Kusz).

    More information can be fount at: https://github.com/mkusz/mkdocs-publisher
    """
    log_level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(level=log_level)


def build_app(app: click.group) -> None:  # type: ignore[reportGeneralTypeIssue]
    plugins_path = pathlib.Path(__file__).parent.resolve() / "plugins"
    for plugin_file_name in pathlib.Path(plugins_path).rglob("*.py"):
        plugin_name = pathlib.PurePath(plugin_file_name).stem
        plugin_module = importlib.import_module(f"mkdocs_publisher._cli.plugins.{plugin_name}")
        app.add_command(cmd=getattr(plugin_module, "app", plugin_name), name=str(plugin_name.replace("_", "-")))


build_app(app=app)


if __name__ == "__main__":
    app()
