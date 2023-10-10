---
title: v1.0.0 - 2023-06-13
slug: v100
publish: published
date: 2023-05-19 15:40:36
update: 2023-10-09 10:28:28
tags:
  - v1.x
description: Publisher for MkDocs v0.6.0
categories:
  - release
---

This was quite a journey to make this release and push it to v1.0.0. So far, this whole documentation was created inside the [Obsidian](https://obsidian.md) but since all the files are just a flat text file written using [Markdown syntax](https://www.markdownguide.org), you were unable to see it. The reason for that was simple: integration with Obsidian was not *"mature"* enough to be presented. You can ask: *"Why? Obsidian just uses the same Markdown syntax as MkDocs uses"*. The answer to that is not so obvious. The simple answer is just *"yes"*, but the real answer is *"not always"*. Obsidian introduces some additional syntax options like [callouts](https://help.obsidian.md/Editing+and+formatting/Callouts) (equivalent to Markdown [admonitions](https://squidfunk.github.io/mkdocs-material/reference/admonitions/)) and [WikiLinks](https://en.wikipedia.org/wiki/Help:Link) for creating internal links. If you use them *"as is"* in MkDocs, you will see a pure (not parsed) text, not the intended one since MkDocs does not understand this syntax. To make it *"understandable"* for MkDocs, it has to be *"translated"* into regular Markdown syntax.

> [!TIP] Translation is non-destructive
> All markdown translations (or rather I should say conversions) are non-destructive to your Obsidian vault and occurs *"on the fly"* while static files are produced. It means that you can use this plugin side-by-side with Obsidian and use, for example, git repository as your vault backup. You don't have to copy or specially prepare your files before using this tool.

For that reason, a new plugin was created, that supports not only the mentioned Obsidian elements, but also some additional ones like:

- [backlinks](https://help.obsidian.md/Plugins/Backlinks),
- [callouts](https://help.obsidian.md/Editing+and+formatting/Callouts),
- [wikilinks](https://help.obsidian.md/Linking+notes+and+files/Internal+links),
- [vega charts](https://vega.github.io/vega/) (using [Vega Visualization Plugin for Obsidian](https://github.com/Some-Regular-Person/obsidian-vega)) - advanced solution for creating charts.

<!-- more -->

If you need support for additional plugins, please make an [issue](https://github.com/mkusz/mkdocs-publisher/issues) with a future description.

For more details about this release, read more below or jump directly to [pub-obsidian](../02_setup/02_general/03_setting-up-obsidian.md) plugin documentation.

I need to start to implement unit tests because this project becomes too big to test it manually and deliver production grade quality. Probably after introducing unit tests, I will end the beta period of this project and consider it as a production ready. It doesn't mean that the project will be complete or free from errors, but at least new releases should not break pages built with this project.

Also from now on all new releases will be smaller. I will try to focus on smaller improvements and fixes, so you should fell like this project is more alive.

Last thing is a new project logo:

<figure markdown>
![MkDocs Publisher logo](../publisher_logo.png)
</figure>

> [!BUG] Known Issues
> List of known issues:
>
> - internal links in blog teasers are not working,
> - using icons in page title, will cause problems with title display in the browser window.

## Changelog

### :material-list-box: General

- :material-plus-circle: internal class for HTML modifications
- :material-sync-circle: project license to MIT
- :material-sync-circle: project `README.md` cleanup
- :material-sync-circle: internal method for importing other plugin config (needed for cross functionalities)

### :material-navigation: Auto-nav (plugin removed)

The whole functionality of this plugin has been moved to a new [Meta plugin](#meta-new-plugin).

### :material-newspaper-variant-multiple: Blog

- :material-plus-circle: exclude from search blog posts teaser/index, category, tag or archive pages
- :material-plus-circle: exclude comments in blog posts teaser/index, category, tag or archive pages
- :material-check-circle: internal links for blog posts teaser/index, category, tag or archive pages
- :material-minus-circle: removed `edit_url` for blog teaser/index, category, tag or archive pages
- :material-sync-circle: automatic detection of the blog as starting page (config value for this setting was removed)
- :material-plus-circle: post publication state (provided by [Meta plugin](#meta-new-plugin))

### :material-share: Social

- :material-sync-circle: code refactor of HTML modification elements and logging added

### :material-file-tree: Meta (new plugin)

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
- :material-plus-circle: while serve page locally, all hidden and draft pages becomes published (this setting, helps with document preview while writing)

### :simple-obsidian: Obsidian (new plugin)

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

---

> [!info] Legend
> :material-plus-circle: - added
>
> :material-minus-circle: - removed
>
> :material-check-circle: - fixed
>
> :material-sync-circle: - changed
