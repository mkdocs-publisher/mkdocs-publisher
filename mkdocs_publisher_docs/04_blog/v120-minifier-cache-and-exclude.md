---
title: v1.2.0 - 2023-10-17
slug: v120
publish: draft
date: 2023-10-17 16:16:39
update: 2023-10-17 17:10:09
tags:
  - v1.x
description:
categories:
  - release
---

This release adds some more control over [minifier](../02_setup/03_seo_and_sharing/02_setting-up-minifier.md) plugin by adding the following settings:

- `cache_enabled` - controls if cache is enabled both globally and per file type (cache is enabled by default),
- `exclude` - list of files and/or directories that are excluded from minification both globally and per file type (by default list of exclusion is empty),
- `extensions` - defines file extensions for each file type.

> [!INFO] Exclusion file name pattern
> `exclude` setting allows defining exact match like `some_file.jpg` or by pattern like `some_jpg_files_in_dir/some*.jpg`. To match all subdirectories, you have to use `**` as a pattern, for example `match_all_files_in_subdirs/**/*`.
> Use it with caution, since using this pattern can be time-consuming (more information can be found at [this link](https://docs.python.org/3/library/pathlib.html#pathlib.Path.glob)).

The [obsidian](../02_setup/02_general/03_setting-up-obsidian.md) plugin, now supports:

- [comments](https://help.obsidian.md/Editing+and+formatting/Basic+formatting+syntax#Comments),
- [MathJax](https://help.obsidian.md/Editing+and+formatting/Advanced+formatting+syntax#Math) - right now you need to [configure it manually](https://squidfunk.github.io/mkdocs-material/reference/math/#mathjax), in the future it will be done automatically when this plugin is enabled,
- [mixed type lists](https://help.obsidian.md/Editing+and+formatting/Basic+formatting+syntax#Lists) - right now you need to [configure it manually](https://python-markdown.github.io/extensions/sane_lists/), in the future it will be done automatically when this plugin is enabled.

I have also added some issue templates on project repository, so if you find some issue or have a future request, fell free to report a [new issue](https://github.com/mkusz/mkdocs-publisher/issues/new/choose).

<!-- more -->

## Changelog

### :simple-obsidian: Obsidian

- ❎ support for comments syntax
- ✅ links for file names with space

### :material-run-fast: Minifier

- ❎ setting for file extensions
- ❎ setting for file exclusion
- ❎ setting for enabling cache
- ✅ extensions are no longer case-sensitive
- ✅ minified file detection is no longer case-sensitive

---

> [!note] Legend
> ❎ - added ✅ - fixed ♻️ - changed 🚫 - removed
