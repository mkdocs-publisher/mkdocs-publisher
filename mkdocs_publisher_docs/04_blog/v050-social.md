---
title: v0.5.0 - 2023-04-04
slug: v050
visibility: published
date: 2023-04-04 21:26:12
update: 2023-08-01 11:51:12
tags:
  - v0.x
description: Publisher for MkDocs v0.5.0
categories:
  - release
---

[Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) has its own [social cards plugin](https://squidfunk.github.io/mkdocs-material/setup/setting-up-social-cards/?h=social), but there are some limitations of it (or rather I should say, their implementation is limiting in some areas). The Material approach to social cards is to generate an image based on document information and requires changing the template manually to add those cards.

**Publisher for MkDocs** uses a different approach to social cards:

- you can set an image per document, but you have to create this image by yourself - it gives you a better control over how it looks like, so it can be more create than the one generated from the template,
- you don't have to change a document template because all the data related to social cards is injected into HTML code of the document while rendering it.

If you need support for additional plugins, please make an [issue](https://github.com/mkusz/mkdocs-publisher/issues) with a future description.

For more details about this release, read more below or jump directly to [pub-social](../02_setup/03_seo_and_sharing/01_setting-up-social-cards.md) plugin documentation.

<!-- more -->

## Changelog

### Blog

- :material-plus-circle: index blog post title is now a link to a post

### Social (new plugin)

- :material-plus-circle: automatic addition of Open Graph tags directly into HTML code (no template modification is needed) based on document meta
- :material-plus-circle: automatic addition of Twitter tags directly into HTML code (no template modification is needed) based on document meta

---

> [!info] Legend
> :material-plus-circle: - added
>
> :material-minus-circle: - removed
>
> :material-check-circle: - fixed
>
> :material-sync-circle: - changed
