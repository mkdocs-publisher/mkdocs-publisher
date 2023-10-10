# MIT License
#
# Copyright (c) 2023 Maciej 'maQ' Kusz <maciej.kusz@gmail.com>
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

import pathlib

import click

from mkdocs_publisher._shared import file_utils


@click.group
def app():
    """Development tools"""
    pass


@app.command()
def css_min():
    """Minify project CSS files"""
    project_dir = pathlib.Path.cwd() / "mkdocs_publisher"
    for input_css_file in project_dir.rglob("*.css"):
        if ".min" not in input_css_file.suffixes:
            output_css_file = input_css_file.parent / f"{input_css_file.stem}.min.css"
            print(output_css_file)
            cmd = [
                "postcss",
                str(input_css_file),
                "-m",
                "--verbose",
                "-u",
                "cssnano",
                "postcss-svgo",
                "-o",
                str(output_css_file),
            ]
            file_utils.run_subprocess(cmd, capture_output=False)
