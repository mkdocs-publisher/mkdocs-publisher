# mkdocs-blog-in

[![PyPI version](https://badge.fury.io/py/mkdocs-blog-in.svg)](https://badge.fury.io/py/mkdocs-blog-in)

This plugin change behaviour of MkDocs, so it allows to use it as a blogging platform.

> **Note**
> As a base for any development, mkdocs-material theme was used.

> **Warning**
> Consider this plugin as a beta, so before any use make sure you have a backup of your data.

If you have found any issue, have an idea for a feature, please submit an issue.

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

This list is unordered so functionalities can be added in whenever upcoming version:

- [ ] add cli tool for creating an empty blog post and page
- [ ] add templates overrides (same mechanism as in mkdocs-material theme) with cli tool to copy a template
- [ ] add social media preview
- [ ] add unittests
- [ ] add page/post meta to publish state like: draft, published, hidden
- [ ] create documentation
- [ ] extend categories functionality like: possibility to add multiple categories (like tags), configurable limit of categories (with checks) and configurable list of categories
- [ ] add configurable date format
- [ ] image optimization (pngquant and jpeg-quantsmooth + mozjpeg) with cache

## Version history

### 0.3.0

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
