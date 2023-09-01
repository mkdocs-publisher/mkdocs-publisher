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
