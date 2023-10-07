---
title: Changelog
icon: material/file-replace-outline
slug: changelog
publish: published
date: 2023-02-12 22:00:00
update: 2023-10-04 13:31:20
description: Publisher for MkDocs version history
categories:
  - general
  - changelog
---

# Version history

## 1.1.1

> :material-plus-circle:{title=added} added
> :material-minus-circle:{title=removed} removed
> :material-check-circle:{title=fixed} fixed
> :material-sync-circle:{title=changed} changed

### :material-list-box: General

- :material-plus-circle: license info added to all project files
- :material-plus-circle: code coverage
- :material-plus-circle: unit test to part of the code (journey begins)
- :material-sync-circle: flake8 linter has been replaced with [ruff](https://github.com/astral-sh/ruff)
- :material-sync-circle: internal code refactoring and simplifications
- :material-sync-circle: project dependencies has been separated into 3 groups: **general**, **test** and **dev**
- :material-sync-circle: main project dependencies has been updated:
	- `mkdocs >= 1.5.3`
	- `mkdocs-material >= 9.4.3`

### :material-newspaper-variant-multiple: Blog

- :material-check-circle: relative links are fixed
- :material-check-circle: meta field `status` collision with [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/reference/#setting-the-page-status) (`>= 9.20`) solved by renaming into `publish` (the same value as in [Obsidian.md](https://help.obsidian.md/Obsidian+Publish/Publish+and+unpublish+notes#Automatically+select+notes+to+publish))

### :material-file-tree: Meta

- :material-check-circle: meta field `status` collision with [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/reference/#setting-the-page-status) (`>= 9.20`) solved by renaming into `publish` (the same value as in [Obsidian.md](https://help.obsidian.md/Obsidian+Publish/Publish+and+unpublish+notes#Automatically+select+notes+to+publish))

### :simple-obsidian: Obsidian

- :material-check-circle: links and wiki links are fixed

### :material-share: Social

### :material-run-fast: Minifier

### :material-shield-bug: Debugger

- :material-check-circle: configuration warnings are now captured and can be part of the log file and new console log look & feel

## 1.1.0 - 2023.09.01

### :material-list-box: General

- :material-sync-circle: rename of directory with documentation files
- :material-sync-circle: Python libraries update
- :material-sync-circle: project naming unification
- :material-sync-circle: pre-commit JSON check and obsidian file exclusion
- :material-sync-circle: some links updates in documentation
- :material-sync-circle: code type hinting updates
- :material-sync-circle: logger names unification - [it's related to pub-debugger plugin](../02_setup/99_development/01_setting-up-debugger.md#python-logging-for-mkdocs)
- :material-sync-circle: code refactor and cleanup
- :material-minus-circle: drop `python-frontmatter` from Python libraries

### :material-newspaper-variant-multiple: Blog

- :material-check-circle: minor fix for internal linking (still not full solution)
- :material-sync-circle: fix for deprecated warning regarding `importlib.resources`

### :material-run-fast: Minifier

- :material-sync-circle: small code reformat related to shared library changes
- :material-sync-circle: files are not minified when using `mkdocs serve` (this is default behavior, but it can be changed)

### :material-file-tree: Meta

- :material-plus-circle: possibility to declare whole directory as hidden
- :material-plus-circle: more logging messages
- :material-plus-circle: better support for `pub-obsidian` plugin (template and obsidian directory are now always drafts)
- :material-check-circle: fix for error with reading `README.md` when no empty line at the end of file
- :material-check-circle: fix for adding again the same directory to draft directories when using `mkdocs serve`

### :simple-obsidian: Obsidian

- :material-check-circle: minor fix for internal linking (still not full fix)
- :material-check-circle: fix for preserving new line in callouts

### :material-shield-bug: Debugger (new plugin)

- :material-plus-circle: console log reformatting with configuration
- :material-plus-circle: added logging into `*.log` file with configuration
- :material-plus-circle: added old log file replacement
- :material-plus-circle: ZIP file creation with log output and some additional files

## 1.0.0 – 2023.06.13

### :material-list-box: General

- :material-plus-circle: internal class for HTML modifications
- :material-plus-circle: project logo
- :material-sync-circle: project license to MIT
- :material-sync-circle: project `README.md` cleanup
- :material-sync-circle: internal method for importing other plugin config (needed for cross functionalities)

### :material-navigation: Auto-nav (plugin removed)

The whole functionality of this plugin has been moved to a new [Meta plugin](#meta-new-plugin).

### :material-newspaper-variant-multiple: Blog

- :material-plus-circle: exclude from search blog posts teaser/index, category, tag or archive pages
- :material-check-circle: internal links for blog posts teaser/index, category, tag or archive pages
- :material-minus-circle: removed `edit_url` for blog teaser/index, category, tag or archive pages
- :material-sync-circle: automatic detection of the blog as starting page (config value for this setting was removed)
- :material-plus-circle: post publication state (provided by [Meta plugin](#meta-new-plugin) )

### :material-share: Social

- :material-sync-circle: code refactor of HTML modification elements and logging added

### :material-file-tree: Meta (new plugin)

This plugin is a Swiss army knife that helps a lot with various tasks related to publication, SEO, etc. Take a look at the below changelog to see what is offered by this plugin.

- :material-plus-circle: build navigation based on file names order
- :material-plus-circle: set multiple document parameters by using its metadata:
	- `title` - document title
	- `slug`- URL of the document
	- `status` - document publication status (published, hidden, draft)
	- `date` - document creation date
	- `update` - document last update date (used for sitemap and SEO optimizations)
- :material-plus-circle: directory metadata and additional settings can be set in a frontmatter of `*.md` file (default to `README.md`):
	 	- possibility to define `slug`(this affects only the directory where `README.md` is placed)
	- possibility to define `skip_dir`(this affects only the directory and all subdirectories where the file is located)
	- possibility to define `hidden_dir`(this affects only the directory and all subdirectories where the file is located)

### :simple-obsidian: Obsidian (new plugin)

This plugin is a set of functionalities and should be split into various smaller plugins, but due to some cross functionalities, it has been integrated into the bigger one. Each sub plugin can be controlled separately, so if you don't need all the functionalities, you can just disable them or simply do not enable one that are disabled by default.

#### General

- :material-plus-circle: server watch can omit `.obsidian` directory that needs to be a part of the documentation directory that is automatically added into watch and causes server reload on (almost) any interaction with obsidian (changing settings etc.)

#### Links

- :material-plus-circle: support for wiki links format for images and internal links
- :material-plus-circle: configurable image lazy loading option (SEO optimization)
- :material-plus-circle: documents and images file path solver (it doesn't affect documentation, but it's required by MkDocs for proper links generation)

#### Callouts

- :material-plus-circle: mapping of all Obsidian callouts into Markdown admonitions

#### Backlinks

- :material-plus-circle: auto-generation of backlinks for all internal documents (visible as an custom admonition at the bottom of the page)
- :material-plus-circle: backlinks are not generated for blog temporary files like post indexes, archive, tags and categories
- :material-plus-circle: backlinks are grouped per page like in Obsidian (if more than one link is pointing from one page to another, all context links will be visible)

#### Charts

- :material-plus-circle: support for *vega* and *vega-lite* charts when added by [Vega Visualization Plugin for Obsidian](https://github.com/Some-Regular-Person/obsidian-vega)

## 0.5.0 – 2023.04.04

### :material-newspaper-variant-multiple: Blog

- :material-plus-circle: index blog post title is now a link to a post

### Social (new plugin)

- :material-plus-circle: automatic addition of open graph tags directly into HTML code (no template modification is needed) based on document meta
- :material-plus-circle: automatic addition of twitter tags directly into HTML code (no template modification is needed) based on document meta

## 0.4.1 - 2023-03-28

### :material-list-box: General

- :material-check-circle: links in documentation
- :material-check-circle: imports of libraries
- :material-check-circle: badges links + new added

## 0.4.0 - 2023-03-28

### :material-list-box: General

- :material-sync-circle: project rename
- :material-plus-circle: cross configuration of blog and auto-nav plugins:
  - blog does not add auto-nav meta files
  - auto-nav automatically adds blog directory to skipped directories since it will be built by blog
  - if one of the plugins is not enabled, other is not using its values

### :material-newspaper-variant-multiple: Blog

- :material-plus-circle: possibility to choose a blog as a starting page with option to define manually blog in nav configuration
- :material-plus-circle:: `slug` config option for setting an entire blog's main directory URL
- :material-sync-circle: internal file structure refactor with new global plugin config (BlogConfig class) that will help with further development with small fixes and improvements
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
- :material-plus-circle: read number of threads from system

### :material-navigation: Auto-nav (new plugin)

- :material-plus-circle: build navigation based on file names
- :material-plus-circle: directory metadata and additional settings can be set in a frontmatter of `*.md` file (default to `README.md`)
- :material-plus-circle: configuration of sort prefix delimiter
- :material-plus-circle: sort prefix removal in URL and site files

## 0.3.0 - 2023.02.20

- :material-check-circle: for wrong directory structure in site-packages after install

## 0.2.0 - 2023.02.20

- :material-plus-circle: sub-pages for archive, categories, blog
- :material-plus-circle: configurable blog posts pagination with page navigation
- :material-plus-circle: interface language change: EN and PL (help wanted with more languages)
- :material-plus-circle: possibility to override for all interface text elements

## 0.1.0 - initial release

- :material-plus-circle: blog post update date based on metadata
- :material-plus-circle: blog post URL link based on metadata
- :material-plus-circle: blog post tags and categories based on metadata
- :material-plus-circle: support for blog post teaser
- :material-plus-circle: auto generation of blog posts navigation

---

> [!info] Legend
> :material-plus-circle:{title=added} added
>
> :material-minus-circle:{title=removed} removed
>
> :material-check-circle:{title=fixed} fixed
>
> :material-sync-circle:{title=changed} changed
