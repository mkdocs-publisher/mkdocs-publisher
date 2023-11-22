---
title: v0.4.0 - 2023-03-28
slug: v040
publish: true
date: 2023-03-28 02:00:00
update: 2023-10-10 13:20:54
tags:
  - v0.x
description: Publisher for MkDocs v0.4.0
categories:
  - release
---

In this release, many things have happened, but the most important one is a project rename.

During a development, many ideas about further development came to my mind. I have created a [backlog](../06_dev/other/02_backlog.md).

<!-- more -->

## Changelog

### :material-list-box: General

- ♻️ project name
- ❎ cross configuration of blog and auto-nav plugins:
	  - blog does not add auto-nav meta files
	  - auto-nav automatically adds blog directory to skipped directories since it will be built by blog
	  - if one of the plugins is not enabled, other is not using its values
- ❎ documentation

### :material-newspaper-variant-multiple: Blog

- ❎ possibility to choose a blog as a starting page with option to define manually blog in nav configuration
- ❎ `slug` config option for setting an entire blog's main directory URL
- ♻️ internal file structure refactor with new global plugin config (`BlogConfig` class) that will help with further development with small fixes and improvements
- ♻️ blog subdirectory navigation creation (entry path needs to be equal to subdirectory name)
- ✅ live reload infinite loop during `serve` caused by temporary files created and removed in blog directory
- ✅ navigation is no longer overridden by a blog (if there is no other nav, blog will create on with recent posts as a main page)

### :material-run-fast: Minifier (new plugin)

- ❎ PNG image minifier (using: pngquant and oxipng)
- ❎ JPG image minifier (using: mozjpeg)
- ❎ SVG image minifier (using: svgo)
- ❎ HTML file minifier (using: html-minifier)
- ❎ CSS file minifier (using: postcss with plugins: cssnano, svgo)
- ❎ JS file minifier (using: uglifyjs)

### :material-navigation: Auto-nav (new plugin)

- ❎ build navigation based on file names
- ❎ directory metadata and additional settings can be set in a frontmatter of `*.md` file (default to `README.md`)
- ❎ configuration of sort prefix delimiter
- ❎ sort prefix removal in URL and site files
- ❎ read file title from `title` metadata key

---

> [!note]
> ❎ - added ✅ - fixed ♻️️ - changed 🚫 - removed
