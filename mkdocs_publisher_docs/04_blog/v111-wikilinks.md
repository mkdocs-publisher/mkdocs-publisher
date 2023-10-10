---
title: v1.1.1 - 2023.10.09
slug: v111
publish: draft
date: 2023-10-09 09:28:53
update: 2023-10-10 12:15:33
tags:
  - v1.x
description:
categories:
  - release
---

This release is probably one of the most important ones for this project, but was also a bit problematic. You can ask why?

The biggest problem that I had, was about numbering this release. Because I wanted to bump all main dependencies (mainly [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/)) i found that one of the metadata key names was colliding with Material for MkDocs and leading to unexpected behavior. I had to change it and for that reason, I was wondering how to handle this event. From one point of view, this is somehow braking change and I should create a v2.0.0, but didn't feel like this is release is big enough. It doesn't include any new functionality and is focused on bug fixes and internal improvements.

> [!DANGER] Publication status key rename
> [Pub-meta](../02_setup/02_general/01_setting-up-meta.md#Document%20publication%20status) document or directory status metadata key has been renamed from `status` to `publish`. This change solves 2 problems:
> 1. Conflict of the key name with [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/reference/?h=status#setting-the-page-status).
> 2. Default name of the key is now the same as for [Obsidian publish](https://help.obsidian.md/Obsidian+Publish/Publish+and+unpublish+notes#Automatically+select+notes+to+publish).
> If you want to use old key name, you are able to do it by [changing key name](../02_setup/02_general/01_setting-up-meta.md#+meta.status.key_name) in `mkdocs.yml` file.

Thanks to [@AgedLace](https://github.com/AgedLace) who is right now the most active user and tester of this project, I managed to fix all the problems with `links` (both wiki and Markdown syntax). There is much more to come in the area of Obsidian syntax support in the near future, like:

- [comments](https://help.obsidian.md/Editing+and+formatting/Basic+formatting+syntax#Comments) - currently not supported,
- [lists](https://help.obsidian.md/Editing+and+formatting/Basic+formatting+syntax#Lists) - supported partially (cannot mix ordered and unordered lists, etc.),
- [page/note preview](https://help.obsidian.md/Plugins/Page+preview) - currently not supported.

I will also create an entire section of the documentation related to Obsidian support (right now there is only a section on [how to set it up](../02_setup/02_general/03_setting-up-obsidian.md)), so stay turned.

Some of you are still waiting for documentation about auto publication using GitHub Actions and some template repository, but it's under development and not yet (fully) ready. If you know how GitHub Actions works, you can take a look at this repository file [depluy pages workflow](https://github.com/mkusz/mkdocs-publisher/blob/main/.github/workflows/deploy-pages.yml). It's used for building this documentation that is pushed into [docs branch](https://github.com/mkusz/mkdocs-publisher/tree/docs) after build. In the future, I'm planning to create a GitHub Action that will do all of it as a single step.

Also, there was a lot of happening in the project backstage like new linter, added unit tests (partly code coverage) and some other small tweaks etc. A lot more things will come in upcoming releases.

<!-- more -->

### :material-list-box: General

- ❎ license info added to all project files
- ❎ code coverage
- ❎ unit test to part of the code (journey begins)
- ♻️️ flake8 linter has been replaced with [ruff](https://github.com/astral-sh/ruff)
- ♻️️ internal code refactoring and simplifications
- ♻️️ project dependencies has been separated into 3 groups: **general**, **test** and **dev**
- ♻️️ main project dependencies has been updated:
	- `mkdocs >= 1.5.3`
	- `mkdocs-material >= 9.4.3`

### :material-newspaper-variant-multiple: Blog

- ✅ relative links are fixed
- ✅ metadata key `status` collision with [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/reference/#setting-the-page-status) (`>= 9.20`) solved by renaming to `publish` (the same value as in [Obsidian.md](https://help.obsidian.md/Obsidian+Publish/Publish+and+unpublish+notes#Automatically+select+notes+to+publish))
- ✅ `temp_dir` default value changed to `.pub_blog_temp`

### :material-file-tree: Meta

- ✅ metadata key `status` collision with [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/reference/#setting-the-page-status) (`>= 9.20`) solved by renaming to `publish` (the same value as in [Obsidian.md](https://help.obsidian.md/Obsidian+Publish/Publish+and+unpublish+notes#Automatically+select+notes+to+publish))

### :material-run-fast: Minifier

- ✅ `cache_dir` default value changed to `.pub_min_cache`

### :simple-obsidian: Obsidian

- ✅ links and wiki links are fixed

### :material-shield-bug: Debugger

- ✅ configuration warnings are now captured and can be part of the log file and new console log look & feel

---

> [!note]
> ❎ - added ✅ - fixed ♻️️ - changed 🚫 - removed
