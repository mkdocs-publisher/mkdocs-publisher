---
title: v0.6.0 - 2023-05-10
slug: v060
status: published
date: 2023-05-10 21:40:36
update: 2023-05-15 16:19:17
tags: [v0.6.0]
description: MkDosc Publisher plugin v0.6.0
categories: release
---

This was quite a journey to make this release. So far, this whole documentation was created inside the [Obsidian](https://obsidian.md) but since all the files are just a flat text file written using [Markdown syntax](https://www.markdownguide.org), you were unable to see it. The reason for that was simple: integration with Obsidian was not "mature" enough to be presented. You can ask: *"Why? Obsidian just uses the same Markdown syntax as MkDocs uses"*. The answer to that is not so obvious. The simple answer is just *"yes"*, but the real answer is *"not always"*. Obsidian introduces some additional syntax options like [callouts](https://help.obsidian.md/Editing+and+formatting/Callouts) (equivalent to Markdown [admonitions](https://squidfunk.github.io/mkdocs-material/reference/admonitions/)) and [WikiLinks](https://en.wikipedia.org/wiki/Help:Link) for creating internal links. If you use them "as is" in MkDocs, you will see a pure (not parsed) text, not the intended one since MkDocs does not understand this syntax. To make it "understandable" for MkDocs, it has to be "translated" into regular Markdown syntax. For that reason, a new plugin was created, that supports not only the mentioned Obsidian elements, but also some additional ones like:

- [backlinks](https://help.obsidian.md/Plugins/Backlinks),
- [callouts](https://help.obsidian.md/Editing+and+formatting/Callouts) ,
- [wikilinks](https://help.obsidian.md/Linking+notes+and+files/Internal+links)
- [vega charts](https://vega.github.io/vega/) (using [Vega Visualization Plugin for Obsidian](https://github.com/Some-Regular-Person/obsidian-vega)) - advanced solution for creating charts,
- mind maps (using [Mindmap NextGen plugin for Obsidian](https://github.com/verocloud/obsidian-mindmap-nextgen)).

If you need support for additional plugins, please make an [issue](https://github.com/mkusz/mkdocs-publisher/issues) with a future description.

For more details about this release, read more below or jump directly to [pub-obsidian](../02_setup/05_setting-up-an-obsidian.md) plugin documentation.


> [!bug] Navigation issue
> There are some problems with the manually created `nav` section. Please use `pub-auto-nav` plugin if you want to use `pub-blog` plugin.

The above bug will be fixed in the next release.

PS. I need to start to implement unit tests because this project becomes too big to test it manually and deliver production grade quality.

<!-- more -->

## Changelog

### General

- :material-plus-circle: internal class for HTML modifications
- :material-sync-circle: project license to MIT
- :material-sync-circle: project `README.md` cleanup
- :material-sync-circle: internal method for importing other plugin config (needed for cross functionalities)

### Auto-nav

- :material-plus-circle: possibility to define `skip_dir` value in `README.md` (this affects only the directory and all subdirectories where the file is located)
- :material-plus-circle: skip directories that name start with `_` (can be configured and disabled)
- :material-check-circle: second level directories were producing double menu entries

### Blog

- :material-check-circle: internal links for blog teaser/index, category, tag or archive pages
- :material-minus-circle: removed `edit_url` for blog teaser/index, category, tag or archive pages

### Social

- :material-sync-circle: code refactor of HTML modification elements and logging added

### Obsidian (new plugin):

This plugin is a set of functionalities and should be split into various smaller plugins, but due to some cross functionalities, it has been integrated into the bigger one. Each sub plugin can be controlled separately, so if you don't need all the functionalities, you can just disable them or simply do not enable one that are disabled by default.

#### General

- :material-plus-circle: server watch can omit `.obsidian` directory that needs to be a part of the documentation directory that is automatically added into watch and causes server reload on (almost) any interaction with obsidian (changing settings etc.)

#### Links

- :material-plus-circle: support for wiki links format for images and internal links
- :material-plus-circle: configurable image lazy loading option (SEO optimization)
- :material-plus-circle: documents and images file path solver (it doesn't affect documentation but it's required by MkDocs for proper links generation)

#### Callouts

- :material-plus-circle: mapping of all Obsidian callouts into Markdown admonitions

#### Backlinks

- :material-plus-circle: auto-generation of backlinks for all internal documents (visible as an custom admonition at the bottom of the page)
- :material-plus-circle: backlinks are not generated for blog temporary files like post indexes, archive, tags and categories
- :material-plus-circle: backlinks are grouped per page like in Obsidian (if more than one link is pointing from one page to another, all context links will be visible)

#### Charts

- :material-plus-circle: support for *vega* and *vega-lite* charts when added by [Vega Visualization Plugin for Obsidian](https://github.com/Some-Regular-Person/obsidian-vega)

### Meta (new plugin):

This plugin is the one that gets some of the functionalities previously implemented in other plugins (like blog) and extends it for more broad usage for rest of the documents. This plugin allows you to set, a various metadata to the generated file like: update date, file and path URL and others. Some of the settings are common for more plugins. Please take a look at the below list and [pub-meta plugin documentation](../02_setup/06_setting-up-a-meta.md).



---

> [!info] Legend
> :material-plus-circle: - added
>
> :material-minus-circle: - removed
>
> :material-check-circle: - fixed
>
> :material-sync-circle: - changed
