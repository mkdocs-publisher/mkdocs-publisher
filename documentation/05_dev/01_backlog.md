---
title: Backlog
slug: backlog
status: published
date: 2023-02-12 22:00:00
update: 2023-04-19 17:59:01
description: Plans for future development of Publisher for MkDocs
categories: general backlog
---

# Plans for future development

Below lists is a list of tasks that are planned to be done (a backlog) and there is no particular order when they will be implemented. If you are interested in any of the below points being implemented in a first place or there is something missing here, please report and issue.

## Plugins

### Auto-nav

There are no development plans at this moment.

### Blog

- [ ] Add: blog post reading time + watch time (defined in post meta)
- [ ] Add: possibility to disable categories and/or tags pages
- [ ] Add: automatic add [search exclude](https://squidfunk.github.io/mkdocs-material/setup/setting-up-site-search/#search-exclusion) to draft and hidden pages when using material for MkDocs theme with search plugin enabled
- [ ] Add: authors and update date in the template
- [ ] Add: blog posts index template override
- [ ] Add: language override in YAML file
- [ ] Add: configurable date format
- [ ] Add: blog post publication state: draft, published, hidden
- [ ] Add: auto-generate slug based on slugify (+ inject into document metadata)
- [ ] Fix: `blog` slug do not open first page when not in standalone mode
- [ ] Fix: remove slug and make it automatically the same as `blog_dir`
- [ ] Fix: if there is a page in `nav` that is right before blog, next page is called `index-0` instead of `blog`
- [ ] Fix: no auto-nav navigation creation

### Minifier

- [ ] Add: ignored files list/pattern (globally and per file type)
- [ ] Add: stats for number of minified/taken from cache files
- [ ] Add: cache disable (globally and per file type)
- [ ] Add: configurable file extensions per minifier

### Automations (new plugin)

- [ ] Add: automatic addition of `extra_css` and `extra_js` files
- [ ] Add: automatic addition of `loading` attribute to all images and iframes for [lazy-loading](https://squidfunk.github.io/mkdocs-material/reference/images/#image-lazy-loading)

### Meta (new plugin)

- [ ] Add: usage of page frontmatter
- [ ] Add: document publication state: draft, published, hidden
- [ ] Add: sitemap optimizations and creation of `robots.txt` file based on document status

### Social

- [ ] Add: image generator if one is not provided
- [ ] Add: ignored file list/pattern
- [ ] Add: warning on missing meta key
- [ ] Add: ignore single file based on frontmatter
- [ ] Add: check for description and title length (SEO)
- [ ] Add: set up a default image used for a social card

### SEO (new plugin)

- [ ] Add: multiple HTML `<meta name="author">` based on frontmatter authors
- [ ] Add: multiple HTML `<meta name="keywords">` based on frontmatter categories and tags
- [ ] Add: publisher HTML value`<link href="{site_url}" rel="publisher" />` that points to the main page URL
- [ ] Add: robots HTML settings `<meta name="robots" content="noindex, nofollow" />`
- [ ] Add: check for description and title length (SEO)

### Obsidian (new plugin)

- [ ] Add: mind maps (using [markmap](https://markmap.js.org/docs/markmap))
- [ ] Add: templates (blog post, page, etc.)
- [ ] Add: graph view (long-term goal)
- [ ] Add: backlinks with unlinked mentions based on page title and aliases (maybe some headings titles?)
- [ ] Add: detection of an `_templates` directory and add it to the auto-nav `skip_dirs`

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

 - [ ] Create Docker image with everything preinstalled and preconfigured
 - [ ] Add to docker image online Vega charts editor
 - [ ] GitHub repo with preconfigured pages, etc. (can be integrated with Docker Image creation)
 - [ ] Unit tests and code coverage with pre-commit
 - [ ] Cleanup list of code TODO's
 - [ ] Drop `python-frontmatter` for MkDocs built-in library for metadata retrieval
 - [ ] Move translations to jinja templates like Material for MkDocs is doing it
