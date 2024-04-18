---
title: v1.3.0 - 2024-04-18
slug: v130
publish: true
date: 2024-04-18 13:43:10
update: 2024-04-18 13:43:10
tags:
  - v1.x
description: Publisher for MkDocs v1.3.0
categories:
  - release
---

It's have been a long journey since last release in October 2023. A lot has happened in my life that is not related to this project, so I didn't have too much time to work on it. But finally, there it is, v1.3.0. Because I wanted to add an overview functionality that will unlock

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

- ❎ adding an overview functionality [Overview](../03_setup/02_general/01_setting-up-meta.md#Overview)
- ❎ slug auto generation if missing in file meta-data ([#63](https://github.com/mkusz/mkdocs-publisher/issues/63))
- ♻️ plugin rewrite + add unitttest

### :simple-obsidian: Obsidian

- ✅ fix for backlinks destroying links additional attributes like title and anchor
- ♻️ some code simplifications and cleanup because of meta plugin rewrite

### :material-shield-bug: Debugger

- ❎ live reload time stamp removed from log message when [show_entry_time](../03_setup/99_development/01_setting-up-debugger.md#+debugger.console.show_entry_time) setting is enabled (its default value)
- ❎ adding the possibility to remove deprecation warnings when [show_deprecation_warnings](../03_setup/99_development/01_setting-up-debugger.md#+debugger.console.show_deprecation_warnings) setting is disabled (its default value)

---

> [!faq] Legend
> ❎ - added ✅ - fixed ♻️ - changed 🚫 - removed
