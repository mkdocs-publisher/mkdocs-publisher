---
title: v1.3.0 - 2024.04.09
slug: v130
publish: true
date: 2024-04-09 14:17:26
update: 2024-04-15 21:26:32
tags:
  - v1.x
description: Publisher for MkDocs v1.3.0
categories:
  - release
---



<!-- more -->

## Changelog

### :material-list-box: General

- ❎ added internal ConfigChoicesEnum class for defining config choices
- ✅ documentation fixes [#61](https://github.com/mkusz/mkdocs-publisher/issues/61)
- ✅ ruff linter settings
- ♻️ isort has been replaced with [ruff](https://github.com/astral-sh/ruff)
- ♻️ assert in unit tests changed to [pytest-check](https://github.com/okken/pytest-check) to use soft assertion functionality

### :material-file-tree: Meta

- ❎ adding an overview functionality [Overview](../03_setup/02_general/01_setting-up-meta.md#Overview)
- ❎ slug auto generation if missing in file meta-data ([#63](https://github.com/mkusz/mkdocs-publisher/issues/63))
- ♻️ plugin rewrite + add unitttest

### :simple-obsidian: Obsidian

- ✅ fix for backlinks destroying links with additional attributes like title and anchor

### :material-shield-bug: Debugger

- ❎ live reload time stamp removed from log message when [show_entry_time](../03_setup/99_development/01_setting-up-debugger.md#+debugger.console.show_entry_time) setting is enabled (it's default value)
- ❎ adding possibility to remove deprecation warnings when [show_deprecation_warnings](../03_setup/99_development/01_setting-up-debugger.md#+debugger.console.show_deprecation_warnings) setting is disabled (it's default value)

---

> [!faq] Legend
> ❎ - added ✅ - fixed ♻️ - changed 🚫 - removed
