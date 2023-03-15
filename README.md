# Publisher plugin for MkDocs

[![PyPI version](https://badge.fury.io/py/mkdocs-blog-in.svg)](https://badge.fury.io/py/mkdocs-blog-in)
[![Github All Releases](https://img.shields.io/github/downloads/mkusz/mkdocs-blog-in/total.svg)]()

Publishing platform plugins for [MkDocs](https://www.mkdocs.org/) that includes:

- pub-auto-nav - building site navigation right from files (no need for manual definition in config)
- pub-blog - adds blogging capability,
- pub-minifier - file size optimization (good for SEO and overall page size optimization).

## Installation

```commandline
pip install mkdocs-publisher
```

## Basic usage

> **Note**
> As a base for any development, mkdocs-material theme was used. If you are willing to use any other theme you may (or may not) face some issues. If this will happen, please submit an issue.

> **Warning**
> Consider this plugin as a beta, so before any use make sure you have a backup of your data.

If you have found any issue, have an idea for a feature, please submit an issue.

## Image optimization

Image optimization is needed for optimal web speed loading that is needed for better scoring on search engines (part of propper SEO). The best image optimization that redeuce image file size but not image quality.

Since 2 most used image formats are PNG and JPEG, this plugin offers image optimization option. Tools used for image optimization were chosen to fulfill both main image optimization purposes: high quality with small file size.

### MacOS installation

- PNG

```commandline
brew install pngquant oxipng
```

- JPEG

```commandline

brew install mozjpeq

```

- SVG

```commandline

brew install svgo

```



## HTML, JS, CSS optimization

```commandline

brew install node
npm install -g html-minifier postcss cssnano postcss-svgo postcss-cli uglify-js

```

## Plugin development

```commandline

poetry add --editable ../mkdocs-publisher/

```

## Features

List of included features (more documentation is needed):

- automatic blog post index page generation with blog post teasers based on delimeter inside a blog post and own template (delimeter can be changed in plugin config in mkdocs.yaml),
- blog post/page update date based on blog post metadata,
- separate directory for blog post documents with auto generated separate navigation (blog posts are sorted from newest to oldest)
- home page set to blog post index with possibility to rename,
- auto adding link to full blog post from blog post index file (under each post that has teaser delimeter, if delimeter is not present, then full post is inside post index file, but is preserved in blog post navigation and site map).
- added sub pages for blog posts: archive, categories, tags

## How To

[TODO]

## Todo's

This list is unordered so functionalities can be added whenever in upcoming version:

- [ ] add: templates overrides (same mechanism as in mkdocs-material theme) with cli tool to copy a template
- [ ] add: social media preview (image metadata key to match RSS plugin defaults)
- [ ] add: obsidian templates and preconfig for new vault
- [ ] add: page/post meta to publish state like: draft, published, hidden
- [ ] add: author/authors per page metadata (with predefined default in mkdocs.yaml)
- [ ] extend: categories functionality like: possibility to add multiple categories (like tags), configurable limit of categories (with checks) and configurable list of categories
- [ ] add: configurable date format
- [ ] add: sitemap optimization + robots.txt (omit pages with 'draft' status, maybe some add 'preview' status (?), check for limits (50MB, 50k links, ), video sitemap, html sitemap, page priority (lowest 0.0 <> 1.0 highest), update frequency, strip blog dynamic pages like tags/categories/archive/etc., https://seosherpa.com/xml-sitemap/)

## Version history

### 0.4.0

General:

- changed: project rename
- added: cross configuration of blog and auto-nav plugins:
  - blog do not add auto-nav meta files
  - auto-nav automatically adds blog dir to skipped directories since it will be build by blog
  - if one of the plugins is not enabled, other is not using it's values

Blog:

- added: possibility to choose a blog as a starting page with option to define manually blog in nav configuration
- added: `slug` config option for setting an entire blog main directory url
- changed: internal file structure refactor with new global plugin config (BlogConfig class) that will help with further development with small fixes and improvements
- changed: blog subdirectory navigation creation (entry path needs to be equal to ssubdirectory name)
- fixed: live reload infinite loop during `serve` caused by temporary files created and removed in blog directory
- fixed: navigation is no longer overriden by a blog (if there is no other nav, blog will create on with recent posts as a main page)

Minifier (new plugin):

- added: png image minifier (using: pngquant and oxipng)
- added: jpg image minifier (using: mozjpeg)
- added: svg image minifier (using: svgo)
- added: html file minifier (using: html-minifier)
- added: css file minifier (using: postcss with plugins: cssnano, svgo)
- added: js file minifier (using: uglifyjs)

Auto-nav (new plugin):

- added: build navigation based on file names
- added: directory metadata and additional settings can be set in a frontmatter of `*.md` file (default to `README.md`)
- added: configuration of sort prefix delimiter
- added: sort prefix removal in url and site files

### 0.3.0 - 2023.02.20

- fixed: for wrong directory structure in site-packages after install

### 0.2.0

- added: sub pages for archive, categories, blog
- added: configurable blog posts pagination with page navigation
- added: interface language change: EN and PL (help wanted with more languages)
- added: possibility to override for all interface text elements

### 0.1.0 - initial release

- added: blog post update date based on metadata
- added: blog post url link based on metadata
- added: blog post tags and categories based on metadata
- added: support for blog post teaser
- added: auto generation of blog posts navigation
