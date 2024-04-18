---
title: Home
slug: .
publish: true
date: 2023-03-12 12:27:00
update: 2024-04-17 20:34:35
description: Installation
categories:
  - start
hide: [toc, navigation]
---

# Publisher for MkDocs

[![License type](https://img.shields.io/github/license/mkusz/mkdocs-publisher?logo=pypi&logoColor=white&style=plastic&label=License)](https://opensource.org/license/mit/)
[![PyPI version](https://img.shields.io/pypi/v/mkdocs-publisher?logo=pypi&logoColor=white&style=plastic&label=PyPi)](https://pypi.org/project/mkdocs-publisher/)
[![PyPI - Python Version](https://img.shields.io/badge/dynamic/toml?url=https%3A%2F%2Fraw.githubusercontent.com%2Fmkusz%2Fmkdocs-publisher%2Fmain%2Fpyproject.toml&query=%24.tool.poetry.dependencies.python&logo=python&logoColor=white&style=plastic&label=Python)](https://www.python.org)
[![PyPI Downloads last month](https://img.shields.io/pypi/dm/mkdocs-publisher?logo=pypi&logoColor=white&style=plastic&label=Downloads)](https://pypistats.org/search/mkdocs-publisher)
[![GitHub last commit](https://img.shields.io/github/last-commit/mkusz/mkdocs-publisher?logo=github&logoColor=white&style=plastic&label=Last%20commit)](https://github.com/mkusz/mkdocs-publisher/commits/main)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white&style=plastic&label=Pre-commit)](https://github.com/pre-commit/pre-commit)
![Code Coverage](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2Fmkusz%2Fmkdocs-publisher%2Fmain%2Fcov.json&query=%24.percent_covered_display&suffix=%25&color=green&style=plastic&label=Code%20coverage)

Publisher for MkDocs is a set of plugins for [MkDocs](https://www.mkdocs.org) that was created originally as “yet another blogging plugin for MkDocs” (you can read more about this in [this blog post](06_blog/v010-initial-release.md)). During a process of development, I realized that it can become something more that will help not only me with blog creation, but also as a part of a wider publishing tool. Documents creation can be used with cooperation with an [Obsidian.md](https://obsidian.md/) that is a tool for creating a second brain and also an excellent Markdown files editor.

Currently, this plugin is also written with strict cooperation with [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) theme. It was not tested on any, and probably some functionalities may not work as intended (for example, formatting of blog posts). However, all the plugins that are included in this package should work separately and not all of them have to be enabled (for example, _pub-minifier_ will work with any other set of plugins).

## Core concepts

Publisher for MkDocs is a set of plugins that was created with the below concepts:

> [!success] User-friendly
> The whole process of installation and configuration should be as simple as possible, so it's harder to get stuck just at the beginning of the way. Most of the settings are predefined the way, that the author of the documentation doesn't have to spend much time on configuration, etc. I know that some elements are still overly complicated, but the development process is not finished, so there is always a room for improvements. On the other hand, this tool will always be limited by the design of the tools that it's relay on. Usually, whenever possible, this tool should simplify the whole process of documentation publication.

> [!success] Optimized for SEO
> All the documents, if created with World Wide Web publication in mind, should be SEO optimized, so they are easier to find by any search engines. SEO it's not only about information that documents contain, but also with some more technical aspects like file size, interlinking, page load time, etc. All those aspects are quite technical one and not always taken into consideration when an author writes any piece of written text. For that reason, this tool is written the way, that the author doesn't have to think about some of those aspects. Some of the aspects are also described in this documentation as part of the documentation process creation.

> [!success] Obsidian.md as first party editor
> Obsidian.md is becoming the tool for creating [Personal Knowledge Management](https://en.wikipedia.org/wiki/Personal_knowledge_management) (PKM) or a [Second Brain](https://www.buildingasecondbrain.com). If you don't know this tool, but you are using any note-taking app like Notion, Evernote, etc. You should definitely try Obsidian. Why? It's because it allows you to achieve much more than any of the above tools and your notes are stored in Markdown files, so it's a great fit for MkDocs since both tools use this format. What's more interesting, Obsidian has lots of community plugins that allow you to achieve more, and some of them are also a great fit for documentation creation and allow you to speed up the process of writing it. This entire documentation was written using Obsidian with all Publisher for MkDocs plugins enabled. You are not forced to use Obsidian for editing, but its worth trying/

## Included features

The list of most important features built into MkDocs Publisher:

- creating a blog posts with automatic build of archive, categories, tags, and index pages ([pub-blog](03_setup/02_general/02_setting-up-blog.md) plugin),
- social cards metadata creation based on document metadata ([pub-social](03_setup/03_seo_and_sharing/01_setting-up-social-cards.md) plugin - :material-plus-circle: [v0.5.0](06_blog/v050-social.md)),
- file size optimizations, that is beneficial for site download speed and SEO ([pub-minifier](03_setup/03_seo_and_sharing/02_setting-up-minifier.md) plugin - :material-plus-circle: [v0.4.0](06_blog/v040-minifier-and-autonav.md)),
- automatic documents navigation creation ([pub-meta](03_setup/02_general/01_setting-up-meta.md) plugin - :material-plus-circle: [v1.0.0](06_blog/v100-obsidian.md)),
- documents publication status with additional meta-data like URL names, etc. beneficial for SEO ([pub-meta](03_setup/02_general/01_setting-up-meta.md) plugin - :material-plus-circle: [v1.0.0](06_blog/v100-obsidian.md)),
- integration with [Obsidian.md](https://obsidian.md/) as documentation editor with support for some Markdown syntax specific to it and some plugins ([pub-obsidian](03_setup/02_general/03_setting-up-obsidian.md) plugin :material-plus-circle: [v1.0.0](06_blog/v100-obsidian.md)):
	- [backlinks](https://help.obsidian.md/Plugins/Backlinks),
	- [callouts](https://help.obsidian.md/Editing+and+formatting/Callouts) ,
	- [wikilinks](https://help.obsidian.md/Linking+notes+and+files/Internal+links),
	- [vega charts](https://vega.github.io/vega/) (using [Vega Visualization Plugin for Obsidian](https://github.com/Some-Regular-Person/obsidian-vega)) - advanced solution for creating charts,
- debugger and logging on steroids - useful for issue reporting and for MkDocs plugin development ([pub-debugger](03_setup/99_development/01_setting-up-debugger.md) plugin :material-plus-circle: [v1.1.0](06_blog/v110-debugger.md)).
