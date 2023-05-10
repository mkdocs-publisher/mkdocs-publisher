---
date: 2023-02-28 12:30:18
update: 2023-04-04 23:52:23
---
# Publisher plugin for MkDocs

[![PyPI version](https://img.shields.io/pypi/v/mkdocs-publisher?logo=pypi&style=plastic)](https://pypi.org/project/mkdocs-publisher/)
[![License type](https://img.shields.io/pypi/l/mkdocs-publisher?logo=pypi&style=plastic)](https://opensource.org/license/mit/)
[![PyPI Downloads last month](https://img.shields.io/pypi/dm/mkdocs-publisher?logo=pypi&style=plastic)](https://pypistats.org/search/mkdocs-publisher)
[![Python versions](https://img.shields.io/pypi/pyversions/mkdocs-publisher?logo=python&style=plastic)](https://www.python.org)
[![GitHub last commit](https://img.shields.io/github/last-commit/mkusz/mkdocs-publisher?logo=github&style=plastic)](https://github.com/mkusz/mkdocs-publisher/commits/main)

Publishing platform plugins for [MkDocs](https://www.mkdocs.org/) that include:

- `pub-auto-nav` – building site navigation right from files (no need for manual definition in config),
- `pub-blog` – adds blogging capability,
- `pub-social` – creates social cards for social media sharing using document metadata,
- `pub-obsidian` - bindings for [Obsidina.md](https://obsidian.md) that allows you to use:
  - wikilinks,
  - backlinks,
  - callouts,
  - vega-charts (plugin),
- `pub-minifier` – file size optimization (good for SEO and overall page size optimization).

## Installation

```commandline
pip install mkdocs-publisher
```

## Basic usage

> **Note**
> As a base for any development, [mkdocs-material](https://squidfunk.github.io/mkdocs-material/) theme was used. If you are willing to use any other theme, you may (or may not) face some issues. If this happens, please submit an [issue](https://github.com/mkusz/mkdocs-publisher/issues).

> **Warning**
> Consider this plugin as a beta, so before any use make sure you have a backup of your data.

If you have found any issue, have an idea for a feature, please submit an issue.

## Features

List of included features (more documentation is needed):

- automatic blog post index page generation with blog post teasers based on delimiter inside a blog post and own template (delimiter can be changed in plugin config in `mkdocs.yaml`),
- blog post/page update date based on blog post metadata,
- separate directory for blog post documents with auto-generated separate navigation (blog posts are sorted from newest to oldest based on blog post metadata),
- home page set to blog post index with possibility to rename,
- auto-adding link to full blog post from blog post index file (under each post that has teaser delimiter, if delimiter is not present, then full post is inside post index file, but is preserved in blog post navigation and site map),
- added sub-pages for blog posts: archive, categories, tags,
- minification plugin for graphics and documentation files,
- social cards metadata injection based on document metadata (no need to edit any template).

## How To

More detailed information on how to set up, configure and write a blog posts and/or documentation can be found in [documentation](https://mkusz.github.io/mkdocs-publisher/) .

## Planned features

A full list of planned developments can be found on [this documentation page](https://mkusz.github.io/mkdocs-publisher/dev/backlog/). I'm planning to move it to the project [GitHub issues](https://github.com/mkusz/mkdocs-publisher/issues) with proper badges and longer descriptions, but it's time-consuming and at this stage I'd rather spend it to develop a project.

## Version history

This section becomes too big and hard to navigate. Also it's harder to maintain the same changelog in 2 places. The entire version history can be found in the project [version history](https://mkusz.github.io/mkdocs-publisher/dev/changelog/) document and on inside project [GitHub releases](https://github.com/mkusz/mkdocs-publisher/releases).
