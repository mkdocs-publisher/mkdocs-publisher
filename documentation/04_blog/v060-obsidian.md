---
title: v0.6.0 - 2023-04-20
slug: v060
status: published
date: 2023-04-20 21:26:12
update: 2023-04-20 12:09:00
tags: [v0.6.0]
description: MkDosc Publisher plugin v0.6.0
categories: release
---

This was quite a journey to make this release. So far, this whole documentation was created inside the [Obsidian](https://obsidian.md) but since all the files are just a flat text file written using [Markdown syntax](https://www.markdownguide.org), you were unable to see it. The reason for that was simple: integration with Obsidian was not "mature" enough to be presented. You can ask: "Why? Obsidian just uses the same Markdown syntax as MkDocs uses.". The answer to that is not so obvious. The simple answer is just "yes", but the real answer is "not always". Obsidian introduces some additional syntax options like [callouts](https://help.obsidian.md/Editing+and+formatting/Callouts) (equivalent to Markdown [admonitions](https://squidfunk.github.io/mkdocs-material/reference/admonitions/)) and [WikiLinks](https://en.wikipedia.org/wiki/Help:Link) for creating internal links. If you use them "as is" in MkDocs, you will see a pure (not parsed) text, not the intended one since MkDocs does not understand this syntax. To make it "understandable" for MkDocs, it has to be "translated" into regular Markdown syntax. For that reason, a new plugin was created, that supports not only the mentioned Obsidian elements, but also some additional ones like:

- [backlinks](https://help.obsidian.md/Plugins/Backlinks),
- charts (using [Vega Visualization Plugin for Obsidian](https://github.com/Some-Regular-Person/obsidian-vega)),
- mind maps (using [Mindmap NextGen plugin for Obsidian](https://github.com/verocloud/obsidian-mindmap-nextgen)).

If you need support for additional plugins, please make an [issue](https://github.com/mkusz/mkdocs-publisher/issues) with a future description.

For more details about this release, read more below or jump directly to [pub-obsidian](../02_setup/05-setting-up-obsidian.md) plugin documentation.

<!-- more -->

## Features implemented

### General

- added: internal class for HTML modifications
- changed: project license to MIT

### Blog

- fixed: internal links for blog teaser/index, category, tag or archive pages
- fixed: remove `edit_url` for blog teaser/index, category, tag or archive pages

### Social

- changed: code refactor of HTML modification elements and logging added

### Obsidian (new plugin):

This plugin is a set of functionalities and should be split into various smaller plugins, but due to some cross functionalities, it has been integrated into the bigger one. Each sub plugin can be controlled separately, so if you don't need all the functionalities, you can just disable them or simply do not enable one that are disabled by default.

#### General

- added: server watch can omit `.obsidian` directory that needs to be a part of the documentation directory that is automatically added into watch and causes server reload on (almost) any interaction with obsidian (changing settings etc.)

#### WikiLinks



#### Callouts

- added: mapping of all Obsidian callouts into Material admonitions

#### Backlinks

- added: auto-generation of backlinks for all internal documents (visible as an custom admonition at the bottom of the page)
- added: backlinks are not generated for blog temporary files like post indexes, archive, tags and categories
- added: backlinks are grouped per page like in Obsidian (if more than one link is pointing from one page to another, all context links will be visible)

#### Charts

- added: support for *vega* and *vega-lite* charts when added by [Vega Visualization Plugin for Obsidian](https://github.com/Some-Regular-Person/obsidian-vega)
-
---

> [!info] Legend
> :material-plus-circle: - added
>
> :material-check-circle: - fixed
>
> :material-sync-circle: - changed
