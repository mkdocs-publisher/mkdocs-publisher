---
title: Changelog
slug: changelog
status: published
date: 2023-02-12 22:00:00
update: 2023-08-01 12:00:33
description: Publisher for MkDocs version history
categories:
  - general
  - changelog
---

# Version history

## 1.1.0 - 2023.09.01

### General

- :material-sync-circle: rename of directory with documentation files
- :material-sync-circle: Python libraries update
- :material-sync-circle: project naming unification
- :material-sync-circle: pre-commit JSON check and obsidian file exclusion
- :material-sync-circle: some links updates in documentation
- :material-sync-circle: code type hinting updates
- :material-sync-circle: logger names unification - [it's related to pub-debugger plugin](../02_setup/99_development/01_setting-up-debugger.md#python-logging-for-mkdocs)
- :material-sync-circle: code refactor and cleanup
- :material-minus-circle: drop `python-frontmatter` from Python libraries

### Blog

- :material-check-circle: minor fix for internal linking (still not full solution)
- :material-sync-circle: fix for deprecated warning regarding `importlib.resources`

### Minifier

- :material-sync-circle: small code reformat related to shared library changes
- :material-sync-circle: files are not minified when using `mkdocs serve` (this is default behavior, but it can be changed)

### Meta

- :material-plus-circle: possibility to declare whole directory as hidden
- :material-plus-circle: more logging messages
- :material-plus-circle: better support for `pub-obsidian` plugin (template and obsidian directory are now always drafts)
- :material-check-circle: fix for error with reading `README.md` when no empty line at the end of file
- :material-check-circle: fix for adding again the same directory to draft directories when using `mkdocs serve`

### Obsidian

- :material-check-circle: minor fix for internal linking (still not full fix)
- :material-check-circle: fix for preserving new line in callouts

### Debugger (new plugin)

- :material-plus-circle: console log reformatting with configuration
- :material-plus-circle: added logging into `*.log` file with configuration
- :material-plus-circle: added old log file replacement
- :material-plus-circle: ZIP file creation with log output and some additional files

## 1.0.0 – 2023.06.13

### General

- :material-plus-circle: internal class for HTML modifications
- :material-plus-circle: project logo
- :material-sync-circle: project license to MIT
- :material-sync-circle: project `README.md` cleanup
- :material-sync-circle: internal method for importing other plugin config (needed for cross functionalities)

### Auto-nav (plugin removed)

The whole functionality of this plugin has been moved to a new [Meta plugin](#meta-new-plugin).

### Blog

- :material-plus-circle: exclude from search blog posts teaser/index, category, tag or archive pages
- :material-check-circle: internal links for blog posts teaser/index, category, tag or archive pages
- :material-minus-circle: removed `edit_url` for blog teaser/index, category, tag or archive pages
- :material-sync-circle: automatic detection of the blog as starting page (config value for this setting was removed)
- :material-plus-circle: post publication state (provided by [Meta plugin](#meta-new-plugin) )

### Social

- :material-sync-circle: code refactor of HTML modification elements and logging added

### Meta (new plugin)

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

### Obsidian (new plugin)

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

### Blog

- add: index blog post title is now a link to a post

### Social (new plugin)

- add: automatic addition of open graph tags directly into HTML code (no template modification is needed) based on document meta
- add: automatic addition of twitter tags directly into HTML code (no template modification is needed) based on document meta

## 0.4.1 - 2023-03-28

### General

- fix: links in documentation
- fix: imports of libraries
- fix: badges links + new added

## 0.4.0 - 2023-03-28

### General

- changed: project rename
- added: cross configuration of blog and auto-nav plugins:
  - blog does not add auto-nav meta files
  - auto-nav automatically adds blog directory to skipped directories since it will be built by blog
  - if one of the plugins is not enabled, other is not using its values

### Blog

- added: possibility to choose a blog as a starting page with option to define manually blog in nav configuration
- added: `slug` config option for setting an entire blog's main directory URL
- changed: internal file structure refactor with new global plugin config (BlogConfig class) that will help with further development with small fixes and improvements
- changed: blog subdirectory navigation creation (entry path needs to be equal to subdirectory name)
- fixed: live reload infinite loop during `serve` caused by temporary files created and removed in blog directory
- fixed: navigation is no longer overridden by a blog (if there is no other nav, blog will create on with recent posts as a main page)

### Minifier (new plugin)

- added: PNG image minifier (using: pngquant and oxipng)
- added: JPG image minifier (using: mozjpeg)
- added: SVG image minifier (using: svgo)
- added: HTML file minifier (using: html-minifier)
- added: CSS file minifier (using: postcss with plugins: cssnano, svgo)
- added: JS file minifier (using: uglifyjs)
- added: read number of threads from system

### Auto-nav (new plugin)

- added: build navigation based on file names
- added: directory metadata and additional settings can be set in a frontmatter of `*.md` file (default to `README.md`)
- added: configuration of sort prefix delimiter
- added: sort prefix removal in URL and site files

## 0.3.0 - 2023.02.20

- fixed: for wrong directory structure in site-packages after install

## 0.2.0 - 2023.02.20

- added: sub-pages for archive, categories, blog
- added: configurable blog posts pagination with page navigation
- added: interface language change: EN and PL (help wanted with more languages)
- added: possibility to override for all interface text elements

## 0.1.0 - initial release

- added: blog post update date based on metadata
- added: blog post URL link based on metadata
- added: blog post tags and categories based on metadata
- added: support for blog post teaser
- added: auto generation of blog posts navigation

---

> [!info] Legend
> :material-plus-circle: - added
>
> :material-minus-circle: - removed
>
> :material-check-circle: - fixed
>
> :material-sync-circle: - changed
