---
title: Home
slug: home
status: published
date: 2023-03-12 12:27:00
categories: start
description: Installation
---
# Publisher plugin for MkDocs

[![PyPI version](https://img.shields.io/pypi/v/mkdocs-publisher?logo=pypi&style=plastic)](https://pypi.org/project/mkdocs-publisher/)
[![License type](https://img.shields.io/pypi/l/mkdocs-publisher?logo=pypi&style=plastic)](https://opensource.org/license/bsd-3-clause/)
[![PyPI Downloads last month](https://img.shields.io/pypi/dm/mkdocs-publisher?logo=pypi&style=plastic)](https://pypistats.org/search/mkdocs-publisher)
[![Python versions](https://img.shields.io/pypi/pyversions/mkdocs-publisher?logo=python&style=plastic)](https://www.python.org)
[![GitHub last commit](https://img.shields.io/github/last-commit/mkusz/mkdocs-publisher?logo=github&style=plastic)](https://github.com/mkusz/mkdocs-publisher/commits/main)

Publisher for MkDocs is a set of plugins for [MkDocs](https://www.mkdocs.org) that was created originally as “yet another blogging plugin for MkDocs” (you can read more about this in [this blog post](04_blog/v010-initial-release.md)). During a process of development, I realized that it can become something more that will help not only me with blog creation, but also as a part of a wider publishing tool. Documents creation can be used with cooperation with an [Obsidian.md](https://obsidian.md/) that is a tool for creating a second brain and also an excellent Markdown files editor.

Currently, this plugin is also written with strict cooperation with [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) theme. It was not tested on any, and probably some functionalities may not work as intended (for example, formatting of blog posts). However, all the plugins that are included in this package should work separately and not all of them have to be enabled (for example, _pub-minifier_ will work with any other set of plugins).

## Included features

The list of most important features built into MkDocs Publisher:

- automatic navigation builds (by using [pub-auto-nav](02_setup/02_setting-up-auto-nav.md) plugin),
- creating a blog posts with automatic build of archive, categories, tags, and index pages (by using [pub-blog](02_setup/03_setting-up-a-blog.md) plugin),
- file size optimizations, that is beneficial for site download speed and SEO (by using [pub-minifier](02_setup/04_setting-up-a-minifier.md) plugin).
