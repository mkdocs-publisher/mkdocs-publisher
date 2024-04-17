# Publisher for MkDocs

[![License type](https://img.shields.io/pypi/l/mkdocs-publisher?logo=pypi&logoColor=white&style=plastic&label=License)](https://opensource.org/license/mit/)
[![PyPI version](https://img.shields.io/pypi/v/mkdocs-publisher?logo=pypi&logoColor=white&style=plastic&label=PyPi)](https://pypi.org/project/mkdocs-publisher/)
[![PyPI - Python Version](https://img.shields.io/badge/dynamic/toml?url=https%3A%2F%2Fraw.githubusercontent.com%2Fmkusz%2Fmkdocs-publisher%2Fmain%2Fpyproject.toml&query=%24.tool.poetry.dependencies.python&logo=python&logoColor=white&style=plastic&label=Python)](https://www.python.org)
[![PyPI Downloads last month](https://img.shields.io/pypi/dm/mkdocs-publisher?logo=pypi&logoColor=white&style=plastic&label=Downloads)](https://pypistats.org/search/mkdocs-publisher)
[![GitHub last commit](https://img.shields.io/github/last-commit/mkusz/mkdocs-publisher?logo=github&logoColor=white&style=plastic&label=Last%20commit)](https://github.com/mkusz/mkdocs-publisher/commits/main)
![Code Coverage](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2Fmkusz%2Fmkdocs-publisher%2Fmain%2Fcov.json&query=%24.percent_covered_display&suffix=%25&color=green&style=plastic&label=Code%20coverage)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white&style=plastic&label=Pre-commit)](https://github.com/pre-commit/pre-commit)

Publisher for [MkDocs](https://www.mkdocs.org/) is a set of plugins that helps with content creation and publication.

## Features

- [pub-meta](https://mkusz.github.io/mkdocs-publisher/setup/general/pub-meta/) – support for:
	- automatic [document navigation](https://www.mkdocs.org/user-guide/configuration/#nav) creation based on file names order,
	- document publication status,
	- possibility to define document and directories URL (good for SEO),
	- document creation and update date (good for SEO),
- [pub-blog](https://mkusz.github.io/mkdocs-publisher/setup/general/pub-blog/) – blogging capability:
	- index creation,
	- support for blog post teasers,
	- automatic creation of pages for archive, categories and tags,
- [pub-obsidian](https://mkusz.github.io/mkdocs-publisher/setup/general/pub-obsidian/) – bindings for [Obsidina.md](https://obsidian.md) that allows you to use:
	- [backlinks](https://help.obsidian.md/Plugins/Backlinks),
	- [callouts](https://help.obsidian.md/Editing+and+formatting/Callouts),
	- [wikilinks](https://help.obsidian.md/Linking+notes+and+files/Internal+links),
	- [vega charts](https://vega.github.io/vega/) (using [Vega Visualization Plugin for Obsidian](https://github.com/Some-Regular-Person/obsidian-vega)) - advanced solution for creating charts,
- [pub-social](https://mkusz.github.io/mkdocs-publisher/setup/seo-and-sharing/pub-social/) – social cards for social media sharing using document metadata,
- [pub-minifier](https://mkusz.github.io/mkdocs-publisher/setup/seo-and-sharing/pub-minifier/) – file size optimization (good for SEO and overall page size optimization),
- [pub-debugger](https://mkusz.github.io/mkdocs-publisher/setup/development/pub-debugger/) – logging on steroids with the possibility of creating of ZIP file with logs and additional information (can be used for better issue reporting).

## Installation

```commandline
pip install mkdocs-publisher
```

More information about installation methods and plugin setup can be found on this [documentation page](https://mkusz.github.io/mkdocs-publisher/setup/installation/).

> [!warning]
> Before any use, make sure you have a backup of your data.

> [!note]
> As a base for any development, [mkdocs-material](https://squidfunk.github.io/mkdocs-material/) theme was used. If you are willing to use any other theme, you may (or may not) face some issues. If this happens, please submit an [issue](https://github.com/mkusz/mkdocs-publisher/issues).

After installation, you have to enable plugins and Material for MkDocs theme in `mkdocs.yml` file:

```yaml
theme: material

plugins:
  - search  # Material for MkDocs search plugin
  - pub-debugger
  - pub-blog
  - pub-obsidian
  - pub-social
  - pub-meta
  - pub-minifier
```

## Planned features

A full list of planned developments can be found on [this documentation page](https://mkusz.github.io/mkdocs-publisher/development/other/backlog/). I'm planning to move it to the project [GitHub issues](https://github.com/mkusz/mkdocs-publisher/issues) with proper badges and longer descriptions, but it's time-consuming and at this stage I'd rather spend it developing a project.

## Version history

The entire version history can be found in the project [version history](https://mkusz.github.io/mkdocs-publisher/development/changelog/) document and inside [releases](https://github.com/mkusz/mkdocs-publisher/releases).
