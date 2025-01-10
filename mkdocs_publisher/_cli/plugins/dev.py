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

import json
import logging
import shutil
from pathlib import Path

import click

from mkdocs_publisher._shared import file_utils

log = logging.getLogger("mkdocs.publisher.cli.dev")


@click.group
def app():
    """Development tools."""
    pass


def iter_res(src_dir: Path, dst_dir: Path, res_path: Path):
    for path in res_path.iterdir():
        if path.is_dir():
            iter_res(src_dir=src_dir, dst_dir=dst_dir, res_path=path)
        else:
            src_file = path
            dst_file = dst_dir / src_file.relative_to(src_dir)
            Path(str(dst_file.parents[0])).mkdir(parents=True, exist_ok=True)
            shutil.copy(src=src_file, dst=dst_file)


@app.command()
def css_min():
    """Minify project CSS files."""
    project_dir = Path.cwd() / "mkdocs_publisher"
    for input_css_file in project_dir.rglob("*.css"):
        if ".min" not in input_css_file.suffixes:
            output_css_file = input_css_file.parent / f"{input_css_file.stem}.min.css"
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


@app.command()
def update_cov():
    """Update cov.json file based on full coverage.json file.

    File cov.json is used by shields.io to display % code coverage in a badge."""
    coverage_file = Path.cwd() / "coverage.json"
    cov_file = Path.cwd() / "cov.json"

    with coverage_file.open(mode="r") as coverage:
        coverage_data = json.load(coverage)["totals"]

    with cov_file.open(mode="w") as cov:
        json.dump(coverage_data, cov, indent=4)
        cov.write("\n")
