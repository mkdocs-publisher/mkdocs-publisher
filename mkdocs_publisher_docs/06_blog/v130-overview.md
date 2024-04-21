---
title: v1.3.0 - 2024-04-18
slug: v130
publish: true
date: 2024-04-18 13:43:10
update: 2024-04-20 23:05:34
tags:
  - v1.x
description: Publisher for MkDocs v1.3.0
categories:
  - release
---

It has been a long journey since the last release in October 2023. A lot has happened in my life that is not related to this project, so I didn't have too much time to work on it. But finally, there it is, v1.3.0.

Because I wanted to add an overview functionality that will unlock the possibility to use [Folder Notes plugin](https://github.com/LostPaul/obsidian-folder-notes) for Obsidian, I had to rewrite almost the whole [meta plugin](../03_setup/02_general/01_setting-up-meta.md). It was a good exercise because it allowed me to simplify the code and add unit tests, so it will be easier to maintain the plugin quality for a longer period of time.

While working on the meta plugin rewrite, I found that some backlinks are not working correctly. Fortunately, I was already working on the meta plugin where all the stuff related to links is living, so I made the fix during the rewrite.

As for unit tests for a whole project, it's just the beginning of the work. So far, I have "only" 179 tests, that covers about 38% of the whole project code. Delivering 100% test coverage will be a hard and time-consuming task, but I will try to raise the bar on each release.

There were also many smaller things added and/or changed inside a project tooling that will help me in the future to maintain good project quality and with new releases.

Unfortunately, I still didn't find much time to work on documentation extension and for preparing a template repository. I feel the need to do it, but those 2 tasks are connected, so probably both of them will be delivered at the same time.

As I'm writing this words, this project is waiting to be added to the [mkdocs catalog](https://github.com/mkdocs/catalog) that is a list of awesome MkDocs plugins. If you like this project, consider adding the star in project [GitHub repository](https://github.com/mkusz/mkdocs-publisher).

<!-- more -->

## Changelog

### :material-list-box: General

- ❎ added internal ConfigChoicesEnum class for defining config choices
- ❎ added code coverage badge with current coverage % value
- ✅ documentation fixes [#61](https://github.com/mkusz/mkdocs-publisher/issues/61)
- ✅ ruff linter settings
- ♻️ isort has been replaced with [ruff](https://github.com/astral-sh/ruff)
- ♻️ assert in unit tests changed to [pytest-check](https://github.com/okken/pytest-check) to use soft assertion functionality

### :material-file-tree: Meta

- ❎ adding an overview functionality [overview](../03_setup/02_general/01_setting-up-meta.md#Overview%20file)
- ❎ slug auto generation if missing in file meta-data ([#63](https://github.com/mkusz/mkdocs-publisher/issues/63))
- ♻️ plugin rewrite + add unitttest

### :simple-obsidian: Obsidian

- ✅ fix for backlinks destroying links additional attributes like title and anchor
- ♻️ some code simplification and cleanup because of meta plugin rewrite

### :material-shield-bug: Debugger

- ❎ live reload time stamp removed from log message when [show_entry_time](../03_setup/99_development/01_setting-up-debugger.md#+debugger.console.show_entry_time) setting is enabled (its default value)
- ❎ adding the possibility to remove deprecation warnings when [show_deprecation_warnings](../03_setup/99_development/01_setting-up-debugger.md#+debugger.console.show_deprecation_warnings) setting is disabled (its default value)

---

> [!faq] Legend
> ❎ - added ✅ - fixed ♻️ - changed 🚫 - removed
