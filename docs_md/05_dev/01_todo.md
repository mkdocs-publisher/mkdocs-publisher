---
title: TODO
slug: todo
status: published
date: 2023-02-12 22:00:00
update: 2023-03-20 18:56:27
categories: general todo
description: Plans for future development of Publisher for MkDocs
---

# Plans for future development

Below TODO lists are an overall plan and there is no particular order when they will be implemented. If you are interested in any of the below points being implemented in a first place or there is something missing here, please report and issue.

## Plugins

### Blog

- [ ] Add: blog post reading time + watch time (defined in post meta)
- [ ] Add: possibility to disable categories and/or tags pages
- [ ] Add: automatic add [search exclude](https://squidfunk.github.io/mkdocs-material/setup/setting-up-site-search/#search-exclusion) to draft and hidden pages when using material for MkDocs theme with search plugin enabled
- [ ] Add: authors and update date in the template
- [ ] Add: blog posts index template override
- [ ] Add: language override in YAML file
- [ ] Add: configurable date format
- [ ] Add: blog post publication state: draft, published, hidden
- [ ] Fix: `blog` slug do not open first page when not in standalone mode

### Minifier

- [ ] Add: ignored files list/pattern (globally and per file type)
- [ ] Add: stats for number of minified/taken from cache files
- [ ] Add: cache disable (globally and per file type)
- [ ] Add: configurable file extensions per minifier

### Automations (new plugin)

- [ ] Add: automatic addition of `extra_css` and `extra_js` files
- [ ] Add: automatic addition of `loading` attribute to all images and iframes for [lazy-loading](https://squidfunk.github.io/mkdocs-material/reference/images/#image-lazy-loading)

### Meta-apply (new plugin)

- [ ] Add: usage of page frontmatter
- [ ] Add: document publication state: draft, published, hidden
- [ ] Add: sitemap optimizations and creation of `robots.txt` file based on document status

### Social (new plugin)

- [ ] Add: inject social media preview into document based on frontmatter

### Obsidian (new plugin)

- [ ] Add: callout format support
- [ ] Add: wiki links format support
- [ ] Add: links fixer relative to file
- [ ] Add: charts
- [ ] Add: mind maps (???)
- [ ] Add: templates (blog post, page, etc.)
- [ ] Add: backlinks
- [ ] Add: graphs (long-term goal)

## General

### CLI tool

- [ ] Add: project initialization that preconfigure `mkdocs.yml`
- [ ] Add: create a new blog post
- [ ] Add: document/blog post slug update
- [ ] Add: check for minifier tools
- [ ] Add: minify single file using minifier
- [ ] Add: document/blog post publication state change

### Documentation

- [ ] Blog plugin
- [ ] Minifier plugin
- [ ] Auto-nav plugin
- [ ] Integration with RSS plugin
- [ ] How to set up and use docker image
- [ ] Setting up CI/CD in GitHub Actions
- [ ] This plugin development how to

### Other

 - [ ] Create Docker image with everything preinstalled and preconfigured
 - [ ] GitHub repo with preconfigured pages, etc. (can be integrated with Docker Image creation)
 - [ ] Unit testss and code coverage with pre-commit
 - [ ] Cleanup list of code TODO's
 - [ ] Drop `python-frontmatter` for MkDocs built-in library for metadata retrieval
