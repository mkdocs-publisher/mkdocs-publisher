---
title: Changelog
slug: changelog
status: published
date: 2023-02-12 22:00:00
update: 2023-03-22 15:46:24
categories: general changelog
description: Publisher for MkDocs version history
---

# Version history

### 0.4.0

General:

- changed: project rename
- added: cross configuration of blog and auto-nav plugins:
  - blog does not add auto-nav meta files
  - auto-nav automatically adds blog directory to skipped directories since it will be built by blog
  - if one of the plugins is not enabled, other is not using its values

Blog:

- added: possibility to choose a blog as a starting page with option to define manually blog in nav configuration
- added: `slug` config option for setting an entire blog's main directory URL
- changed: internal file structure refactor with new global plugin config (BlogConfig class) that will help with further development with small fixes and improvements
- changed: blog subdirectory navigation creation (entry path needs to be equal to subdirectory name)
- fixed: live reload infinite loop during `serve` caused by temporary files created and removed in blog directory
- fixed: navigation is no longer overridden by a blog (if there is no other nav, blog will create on with recent posts as a main page)

Minifier (new plugin):

- added: PNG image minifier (using: pngquant and oxipng)
- added: JPG image minifier (using: mozjpeg)
- added: SVG image minifier (using: svgo)
- added: HTML file minifier (using: html-minifier)
- added: CSS file minifier (using: postcss with plugins: cssnano, svgo)
- added: JS file minifier (using: uglifyjs)
- added: read number of threads from system

Auto-nav (new plugin):

- added: build navigation based on file names
- added: directory metadata and additional settings can be set in a frontmatter of `*.md` file (default to `README.md`)
- added: configuration of sort prefix delimiter
- added: sort prefix removal in URL and site files

### 0.3.0 - 2023.02.20

- fixed: for wrong directory structure in site-packages after install

### 0.2.0 - 2023.02.20

- added: sub-pages for archive, categories, blog
- added: configurable blog posts pagination with page navigation
- added: interface language change: EN and PL (help wanted with more languages)
- added: possibility to override for all interface text elements

### 0.1.0 - initial release

- added: blog post update date based on metadata
- added: blog post URL link based on metadata
- added: blog post tags and categories based on metadata
- added: support for blog post teaser
- added: auto generation of blog posts navigation
