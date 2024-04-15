---
title: Changelog
icon: material/file-replace-outline
slug: changelog
publish: true
date: 2023-02-12 22:00:00
update: 2024-04-15 21:00:52
description: Publisher for MkDocs version history
categories:
  - general
  - changelog
---

# Version history

## 1.3.0

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

- ✅ fix for backlinks destroying links additional attributes like title and anchor

### :material-shield-bug: Debugger

- ❎ live reload time stamp removed from log message when [show_entry_time](../03_setup/99_development/01_setting-up-debugger.md#+debugger.console.show_entry_time) setting is enabled (it's default value)
- ❎ adding possibility to remove deprecation warnings when [show_deprecation_warnings](../03_setup/99_development/01_setting-up-debugger.md#+debugger.console.show_deprecation_warnings) setting is disabled (it's default value)

## 1.2.0 - 2023-10-17

### :simple-obsidian: Obsidian

- ❎ support for comments syntax
- ✅ links for file names with space

### :material-run-fast: Minifier

- ❎ setting for file extensions
- ❎ setting for file exclusion
- ❎ setting for enabling cache
- ✅ extensions are no longer case-sensitive
- ✅ minified file detection is no longer case-sensitive

## 1.1.1 - 2023-10-10

### :material-list-box: General

- ❎ license info added to all project files
- ❎ code coverage
- ❎ unit test to part of the code (journey begins)
- ♻️ flake8 linter has been replaced with [ruff](https://github.com/astral-sh/ruff)
- ♻️ internal code refactoring and simplifications
- ♻️ project dependencies have been separated into 3 groups: **general**, **test** and **dev**
- ♻️ main project dependencies has been updated:
	- `mkdocs >= 1.5.3`
	- `mkdocs-material >= 9.4.3`

### :material-newspaper-variant-multiple: Blog

- ✅ relative links are fixed
- ✅ metadata key `status` collision with [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/reference/#setting-the-page-status) (`>= 9.20`) solved by renaming to `publish` (the same value as in [Obsidian.md](https://help.obsidian.md/Obsidian+Publish/Publish+and+unpublish+notes#Automatically+select+notes+to+publish))

### :material-file-tree: Meta

- ✅ metadata key `status` collision with [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/reference/#setting-the-page-status) (`>= 9.20`) solved by renaming to `publish` (the same value as in [Obsidian.md](https://help.obsidian.md/Obsidian+Publish/Publish+and+unpublish+notes#Automatically+select+notes+to+publish))

### :simple-obsidian: Obsidian

- ✅ links and wiki links are fixed

### :material-shield-bug: Debugger

- ✅ configuration warnings are now captured and can be part of the log file and new console log look & feel

## 1.1.0 - 2023.09.01

### :material-list-box: General

- ♻️ rename of directory with documentation files
- ♻️ Python libraries update
- ♻️ project naming unification
- ♻️ pre-commit JSON check and obsidian file exclusion
- ♻️ some links updates in documentation
- ♻️ code type hinting updates
- ♻️ logger names unification - [it's related to pub-debugger plugin](../03_setup/99_development/01_setting-up-debugger.md#python-logging-for-mkdocs)
- ♻️ code refactor and cleanup
- 🚫 drop `python-frontmatter` from Python libraries

### :material-newspaper-variant-multiple: Blog

- ✅ minor fix for internal linking (still not full solution)
- ♻️ fix for deprecated warning regarding `importlib.resources`

### :material-run-fast: Minifier

- ♻️ small code reformat related to shared library changes
- ♻️ files are not minified when using `mkdocs serve` (this is default behavior, but it can be changed)

### :material-file-tree: Meta

- ❎ possibility to declare whole directory as hidden
- ❎ more logging messages
- ❎ better support for `pub-obsidian` plugin (template and obsidian directory are now always drafts)
- ✅ fix for error with reading `README.md` when no empty line at the end of file
- ✅ fix for adding again the same directory to draft directories when using `mkdocs serve`

### :simple-obsidian: Obsidian

- ✅ minor fix for internal linking (still not full fix)
- ✅ fix for preserving new line in callouts

### :material-shield-bug: Debugger (new plugin)

- ❎ console log reformatting with configuration
- ❎ added logging into `*.log` file with configuration
- ❎ added old log file replacement
- ❎ ZIP file creation with log output and some additional files

## 1.0.0 – 2023.06.13

### :material-list-box: General

- ❎ internal class for HTML modifications
- ❎ project logo
- ♻️ project license to MIT
- ♻️ project `README.md` cleanup
- ♻️ internal method for importing other plugin config (needed for cross functionalities)

### :material-navigation: Auto-nav (plugin removed)

The whole functionality of this plugin has been moved to a new [Meta plugin](#meta-new-plugin).

### :material-newspaper-variant-multiple: Blog

- ❎ exclude from search blog posts teaser/index, category, tag or archive pages
- ✅ internal links for blog posts teaser/index, category, tag or archive pages
- 🚫 removed `edit_url` for blog teaser/index, category, tag or archive pages
- ♻️ automatic detection of the blog as starting page (config value for this setting was removed)
- ❎ post publication state (provided by [Meta plugin](#meta-new-plugin) )

### :material-share: Social

- ♻️ code refactor of HTML modification elements and logging added

### :material-file-tree: Meta (new plugin)

This plugin is a Swiss army knife that helps a lot with various tasks related to publication, SEO, etc. Take a look at the below changelog to see what is offered by this plugin.

- ❎ build navigation based on file names order
- ❎ set multiple document parameters by using its metadata:
	- `title` - document title
	- `slug`- URL of the document
	- `status` - document publication status (published, hidden, draft)
	- `date` - document creation date
	- `update` - document last update date (used for sitemap and SEO optimizations)
- ❎ directory metadata and additional settings can be set in a frontmatter of `*.md` file (default to `README.md`):
	 	- possibility to define `slug`(this affects only the directory where `README.md` is placed)
	- possibility to define `skip_dir`(this affects only the directory and all subdirectories where the file is located)
	- possibility to define `hidden_dir`(this affects only the directory and all subdirectories where the file is located)

### :simple-obsidian: Obsidian (new plugin)

This plugin is a set of functionalities and should be split into various smaller plugins, but due to some cross functionalities, it has been integrated into the bigger one. Each sub plugin can be controlled separately, so if you don't need all the functionalities, you can just disable them or simply do not enable one that are disabled by default.

#### General

- ❎ server watch can omit `.obsidian` directory that needs to be a part of the documentation directory that is automatically added into watch and causes server reload on (almost) any interaction with obsidian (changing settings etc.)

#### Links

- ❎ support for wiki links format for images and internal links
- ❎ configurable image lazy loading option (SEO optimization)
- ❎ documents and images file path solver (it doesn't affect documentation, but it's required by MkDocs for proper links generation)

#### Callouts

- ❎ mapping of all Obsidian callouts into Markdown admonitions

#### Backlinks

- ❎ auto-generation of backlinks for all internal documents (visible as an custom admonition at the bottom of the page)
- ❎ backlinks are not generated for blog temporary files like post indexes, archive, tags and categories
- ❎ backlinks are grouped per page like in Obsidian (if more than one link is pointing from one page to another, all context links will be visible)

#### Charts

- ❎ support for *vega* and *vega-lite* charts when added by [Vega Visualization Plugin for Obsidian](https://github.com/Some-Regular-Person/obsidian-vega)

## 0.5.0 – 2023.04.04

### :material-newspaper-variant-multiple: Blog

- ❎ index blog post title is now a link to a post

### Social (new plugin)

- ❎ automatic addition of open graph tags directly into HTML code (no template modification is needed) based on document meta
- ❎ automatic addition of twitter tags directly into HTML code (no template modification is needed) based on document meta

## 0.4.1 - 2023-03-28

### :material-list-box: General

- ✅ links in documentation
- ✅ imports of libraries
- ✅ badges links + new added

## 0.4.0 - 2023-03-28

### :material-list-box: General

- ♻️ project rename
- ❎ cross configuration of blog and auto-nav plugins:
  - blog does not add auto-nav meta files
  - auto-nav automatically adds blog directory to skipped directories since it will be built by blog
  - if one of the plugins is not enabled, other is not using its values

### :material-newspaper-variant-multiple: Blog

- ❎ possibility to choose a blog as a starting page with option to define manually blog in nav configuration
- ❎: `slug` config option for setting an entire blog's main directory URL
- ♻️ internal file structure refactor with new global plugin config (BlogConfig class) that will help with further development with small fixes and improvements
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
- ❎ read number of threads from system

### :material-navigation: Auto-nav (new plugin)

- ❎ build navigation based on file names
- ❎ directory metadata and additional settings can be set in a frontmatter of `*.md` file (default to `README.md`)
- ❎ configuration of sort prefix delimiter
- ❎ sort prefix removal in URL and site files

## 0.3.0 - 2023.02.20

- ✅ wrong directory structure in site-packages after install

## 0.2.0 - 2023.02.20

- ❎ sub-pages for archive, categories, blog
- ❎ configurable blog posts pagination with page navigation
- ❎ interface language change: EN and PL (help wanted with more languages)
- ❎ possibility to override for all interface text elements

## 0.1.0 - initial release

- ❎ blog post update date based on metadata
- ❎ blog post URL link based on metadata
- ❎ blog post tags and categories based on metadata
- ❎ support for blog post teaser
- ❎ auto generation of blog posts navigation

---

> [!note]
> ❎ - added ✅ - fixed ♻️️ - changed 🚫 - removed
