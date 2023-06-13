---
title: Backlog
slug: backlog
status: published
date: 2023-02-12 22:00:00
update: 2023-06-12 14:00:07
description: Plans for future development of Publisher for MkDocs
categories: general backlog
---

# Plans for future development

Below lists is a list of tasks that are planned to be done (a backlog) and there is no particular order when they will be implemented. If you are interested in any of the below points being implemented in a first place or there is something missing here, please report and issue.

## Plugins

### Blog

- [ ] Add: blog post reading time + watch time (defined in post meta)
- [ ] Add: possibility to disable categories and/or tags pages
- [ ] Add: authors and update date in the template
- [ ] Add: blog posts index template override
- [ ] Add: language override in YAML file
- [ ] Add: configurable date format
- [ ] Add: auto-generate slug based on slugify (+ inject into document metadata)
- [ ] Change: detect if meta plugin is enabled and based on its configuration use key names
- [ ] Add: possibility to define blog directory in `README.md` file when meta plugin is enabled
- [ ] Fix: links when using meta plugin and slugs on post teasers
- [ ] Fix: internal links in teasers
- [ ] Change: temporary file location

### Minifier

- [ ] Add: ignored files list/pattern (globally and per file type)
- [ ] Add: stats for number of minified/taken from cache files
- [ ] Add: cache disable (globally and per file type)
- [ ] Add: configurable file extensions per minifier
- [ ] Add: documentation for specific settings per file type
- [ ] Add: support for WebP files

### Meta

- [ ] Add: sitemap optimizations and creation of `robots.txt` file based on document status
- [ ] Add: multiple HTML `<meta name="author">` based on frontmatter authors
- [ ] Add: multiple HTML `<meta name="keywords">` based on frontmatter categories and tags
- [ ] Add: publisher HTML value`<link href="{site_url}" rel="publisher" />` that points to the main page URL
- [ ] Add: robots HTML settings `<meta name="robots" content="noindex, nofollow" />`
- [ ] Add: check for description and title length (SEO)
- [ ] Add: turn off auto nav creation setting
- [ ] Add: navigation links using `README.md` in fake directory (directory is needed to preserve order of an auto navigation builder)
- [ ] Add: dynamically generate pages for tags and categories for all documents (just like in blog)
- [ ] Add: nav name metadata (just like in blog)
- [ ] Add: configurable key and format for creation and update date of the document

### Social

- [ ] Add: image generator if one is not provided
- [ ] Add: ignored file list/pattern
- [ ] Add: warning on missing meta key
- [ ] Add: ignore single file based on metadata
- [ ] Add: check for description and title length (SEO)
- [ ] Add: set up a default image used for a social card
- [ ] Add: metadata key names from meta plugin
- [ ] Change: detect if meta plugin is enabled and based on its configuration use key names

### Obsidian

- [ ] Add: mind maps (using [markmap](https://markmap.js.org/docs/markmap))
- [ ] Add: simpler charts (using [chart.js](https://www.chartjs.org/docs/latest/samples/bar/border-radius.html))
- [ ] Add: templates (blog post, page, etc.)
- [ ] Add: graph view (long-term goal)
- [ ] Add: backlinks with unlinked mentions based on page title and aliases (maybe some headings titles?)
- [ ] Add: disable backlinks on given page (meta-data: `backlinks: false`)
- [ ] Add: configurable aliases in callouts with auto-add to Obsidian CSS files
- [ ] Change: backlink anchor link creation using slug information

## General

### CLI tool

- [ ] Add: project initialization that preconfigure `mkdocs.yml`
- [ ] Add: create a new blog post
- [ ] Add: document/blog post slug update
- [ ] Add: check for minifier tools
- [ ] Add: clean minifier cache
- [ ] Add: minify single file using minifier
- [ ] Add: document/blog post publication state change
- [ ] Add: CONTRIBUTING.md file to the repo
- [ ] Add: issues templates in the project repository issues

### Documentation

- [ ] Auto-nav plugin
- [ ] Integration with RSS plugin
- [ ] How to set up and use docker image
- [ ] Setting up CI/CD in GitHub Actions
- [ ] This plugin development how to
- [ ] Credits for used libraries with description (like in [MkDocs Coverage Plugin](https://pawamoy.github.io/mkdocs-coverage/credits/))

### Other

 - [ ] Create a Docker image with everything preinstalled and preconfigured
 - [ ] Add to docker image online Vega charts editor
 - [ ] GitHub repo with preconfigured pages, etc. (can be integrated with Docker Image creation)
 - [ ] Unit tests and code coverage with pre-commit
 - [ ] Cleanup list of code TODO's
 - [ ] Drop `python-frontmatter` for MkDocs built-in library for metadata retrieval
 - [ ] Review `importlib.resources` for [deprecated functions](https://docs.python.org/3/library/importlib.resources.html)
 - [ ] Move translations to jinja templates like Material for MkDocs is doing it
