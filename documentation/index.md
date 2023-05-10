---
title: Home
slug: home
status: published
date: 2023-03-12 12:27:00
update: 2023-04-21 14:53:51
description: Installation
categories: start
---
# Publisher plugin for MkDocs

[![PyPI version](https://img.shields.io/pypi/v/mkdocs-publisher?logo=pypi&style=plastic)](https://pypi.org/project/mkdocs-publisher/)
[![License type](https://img.shields.io/pypi/l/mkdocs-publisher?logo=pypi&style=plastic)](https://opensource.org/license/bsd-2-clause/)
[![PyPI Downloads last month](https://img.shields.io/pypi/dm/mkdocs-publisher?logo=pypi&style=plastic)](https://pypistats.org/search/mkdocs-publisher)
[![Python versions](https://img.shields.io/pypi/pyversions/mkdocs-publisher?logo=python&style=plastic)](https://www.python.org)
[![GitHub last commit](https://img.shields.io/github/last-commit/mkusz/mkdocs-publisher?logo=github&style=plastic)](https://github.com/mkusz/mkdocs-publisher/commits/main)

Publisher for MkDocs is a set of plugins for [MkDocs](https://www.mkdocs.org) that was created originally as “yet another blogging plugin for MkDocs” (you can read more about this in [this blog post](04_blog/v010-initial-release.md)). During a process of development, I realized that it can become something more that will help not only me with blog creation, but also as a part of a wider publishing tool. Documents creation can be used with cooperation with an [Obsidian.md](https://obsidian.md/) that is a tool for creating a second brain and also an excellent Markdown files editor.

Currently, this plugin is also written with strict cooperation with [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) theme. It was not tested on any, and probably some functionalities may not work as intended (for example, formatting of blog posts). However, all the plugins that are included in this package should work separately and not all of them have to be enabled (for example, _pub-minifier_ will work with any other set of plugins).

## Included features

The list of most important features built into MkDocs Publisher:

- automatic navigation builds ([pub-auto-nav](02_setup/02_setting-up-auto-nav.md) plugin - :material-plus-circle: [v0.4.0](04_blog/v040-minifier-and-autonav.md)),
- creating a blog posts with automatic build of archive, categories, tags, and index pages ([pub-blog](02_setup/03_setting-up-a-blog.md) plugin),
- social cards metadata creation based on document metadata ([pub-social](02_setup/04_setting-up-a-social-cards.md) plugin - :material-plus-circle: [v0.5.0](04_blog/v050-social.md)),
- file size optimizations, that is beneficial for site download speed and SEO ([pub-minifier](02_setup/09_setting-up-a-minifier.md) plugin - :material-plus-circle: [v0.4.0](04_blog/v040-minifier-and-autonav.md)),
- integration with [Obsidian.md](https://obsidian.md/) as documentation editor with support for some Markdown syntax specific to it and some plugins ([pub-obsidian](02_setup/05-setting-up-obsidian.md) plugin :material-plus-circle: [v0.6.0](04_blog/v060-obsidian.md)):
	- [backlinks](https://help.obsidian.md/Plugins/Backlinks),
	- [callouts](https://help.obsidian.md/Editing+and+formatting/Callouts) ,
	- [wikilinks](https://help.obsidian.md/Linking+notes+and+files/Internal+links)
	- [vega charts](https://vega.github.io/vega/) (using [Vega Visualization Plugin for Obsidian](https://github.com/Some-Regular-Person/obsidian-vega)) - advanced solution for creating charts,
	- mind maps (using [Mindmap NextGen plugin for Obsidian](https://github.com/verocloud/obsidian-mindmap-nextgen)).
