---
title: v0.4.0 - 2023-03-28
slug: v040
publish: published
date: 2023-03-28 02:00:00
update: 2023-10-09 10:29:06
tags:
  - v0.x
description: Publisher for MkDocs v0.4.0
categories:
  - release
---

In this release, many things have happened, but the most important one is a project rename.

During a development, many ideas about further development came to my mind. I have created a [backlog](../05_dev/other/02_backlog.md).

<!-- more -->

## Changelog

### :material-list-box: General

- :material-sync-circle: project name
- :material-plus-circle: cross configuration of blog and auto-nav plugins:
	  - blog does not add auto-nav meta files
	  - auto-nav automatically adds blog directory to skipped directories since it will be built by blog
	  - if one of the plugins is not enabled, other is not using its values
- :material-plus-circle: documentation

### :material-newspaper-variant-multiple: Blog

- :material-plus-circle: possibility to choose a blog as a starting page with option to define manually blog in nav configuration
- :material-plus-circle: `slug` config option for setting an entire blog's main directory URL
- :material-sync-circle: internal file structure refactor with new global plugin config (`BlogConfig` class) that will help with further development with small fixes and improvements
- :material-sync-circle: blog subdirectory navigation creation (entry path needs to be equal to subdirectory name)
- :material-check-circle: live reload infinite loop during `serve` caused by temporary files created and removed in blog directory
- :material-check-circle: navigation is no longer overridden by a blog (if there is no other nav, blog will create on with recent posts as a main page)

### :material-run-fast: Minifier (new plugin)

- :material-plus-circle: PNG image minifier (using: pngquant and oxipng)
- :material-plus-circle: JPG image minifier (using: mozjpeg)
- :material-plus-circle: SVG image minifier (using: svgo)
- :material-plus-circle: HTML file minifier (using: html-minifier)
- :material-plus-circle: CSS file minifier (using: postcss with plugins: cssnano, svgo)
- :material-plus-circle: JS file minifier (using: uglifyjs)

### :material-navigation: Auto-nav (new plugin)

- :material-plus-circle: build navigation based on file names
- :material-plus-circle: directory metadata and additional settings can be set in a frontmatter of `*.md` file (default to `README.md`)
- :material-plus-circle: configuration of sort prefix delimiter
- :material-plus-circle: sort prefix removal in URL and site files
- :material-plus-circle: read file title from `title` metadata key

---

> [!info] Legend
> :material-plus-circle: - added
>
> :material-minus-circle: - removed
>
> :material-check-circle: - fixed
>
> :material-sync-circle: - changed
