---
title: Setting up Obsidian
slug: pub-obsidian
status: published
date: 2023-04-20 12:07:21
update: 2023-08-12 21:13:31
description: Setting up a Publisher for MkDocs obsidian plugin for integration with an Obsidian note taking tool
categories:
  - setup
  - plugin
  - obsidian
---

# Setting up Obsidian

## Introduction

When you want to create some documentation, you need some tools that will help you with writing it. There are multiple ways of achieving it and one of them is to write documentation using flat files using Markdown syntax. This syntax is utilized not only by MkDocs, but also by other tools like [Obsidian](https://obsidian.md). In general, Obsidian is a note-taking app, but because it's a very flexible tool, it's quite often used for creating [Personal Knowledge Management](https://en.wikipedia.org/wiki/Personal_knowledge_management) or a [Second Brain](https://www.buildingasecondbrain.com).

Obsidian introduces some additional Markdown syntax options like [callouts](https://help.obsidian.md/Editing+and+formatting/Callouts) (equivalent to Markdown [admonitions](https://squidfunk.github.io/mkdocs-material/reference/admonitions/)) and [WikiLinks](https://en.wikipedia.org/wiki/Help:Link) for creating internal links. Those internal links, in Obsidian, give you additional functionality of an automatic [backlinks](https://help.obsidian.md/Plugins/Backlinks) that just create a link to a document that mentions the document you are now reading. This way, you can have a better understanding of the relation in between 2 documents or topics that are described in them. If you want to know how the backlinks looks like, take a look at the bottom of this page.

Also, Obsidian has a huge variety of additional plugins, that allow to add some additional elements to the document, like charts, etc. Currently, the obsidian plugin, supports:

- [Vega charts plugin](https://github.com/Justin-J-K/obsidian-vega) - this plugin allows for adding [Vega Charts](https://vega.github.io/vega/).

Support for more plugins is [coming soon](../../05_dev/other/02_backlog.md).

## Creating Obsidian Vault

The most important thing if you want to use Obsidian as an IDE for creating a documentation, you have to [create an Obsidian Vault](https://help.obsidian.md/Getting+started/Create+a+vault) inside a `docs` directory.

When the vault is created, inside `docs` directory, there will be created an `.obsidian` directory. This directory contains some Obsidian files with the app settings, additional files, etc.

```console hl_lines="2-3"
.
├─ docs/
│  └─ .obsidian/
└─ mkdocs.yml
```

> [!Warning] `.obsdian` directory
> This directory can contain some crucial information, like paid Obsidian plugins credentials, etc. If you are using any git repository for storing your documentation, consider adding this directory into [.gitignore](https://git-scm.com/docs/gitignore) to avoid potential security problems.
> Do not remove this directory because you will lose your vault settings.

## Obsidian templates

One of the benefits of using Obsidian, is the possibility to define and use templates for the whole document structure or parts of the document. To make use of the templates, you have create a template directory in `docs` directory and then [set up the template plugin in Obsidian](https://help.obsidian.md/Plugins/Templates) with the same template directory. By default, this directory name is set to `_templates`.

```console hl_lines="2 4"
.
├─ docs/
│  ├─ .obsidian/
|  └─ _templates/
└─ mkdocs.yml
```

## Configuration

To enable the built-in obsidian plugin, the following lines have to be added to `mkdocs.yml` file:

===+ ":octicons-file-code-16: mkdocs.yml"

    ```yaml hl_lines="2"
    plugins:
      - pub-obsidian
    ```

### General

===+ ":octicons-file-code-16: mkdocs.yml"

``` yaml hl_lines="3-4"
plugins:
  - pub-obsidian:
	obsidian_dir: .obsidian
	templates_dir: _templates
```

Above you can find all possible settings with their default values. You don't have to provide them. Just use them if you want to change some settings. The description of the meaning of given setting, you can find below.

> [!SETTINGS]- [obsidian_dir](#+obsidian.obsidian_dir){#+obsidian.obsidian_dir}
> Defines the name of an Obsidian directory, where all the setting files are stored.

> [!SETTINGS]- [templates_dir](#+obsidian.templates_dir){#+obsidian.templates_dir}
> Defines the name of an Obsidian directory, where all the note templates files are stored.

### Backlinks

===+ ":octicons-file-code-16: mkdocs.yml"

``` yaml hl_lines="3-4"
plugins:
  - pub-obsidian:
	backlinks:
	  enabled: true
```

Above you can find all possible settings with their default values. You don't have to provide them. Just use them if you want to change some settings. The description of the meaning of given setting, you can find below.

> [!SETTINGS]- [enabled](#+obsidian.backlinks.enabled){#+obsidian.backlinks.enabled}
> Control if backlinks are generated on the document web page.

### Callouts

===+ ":octicons-file-code-16: mkdocs.yml"

``` yaml hl_lines="3-5"
plugins:
  - pub-obsidian:
	callouts:
	  enabled: true
	  indentation: spaces
```

Above you can find all possible settings with their default values. You don't have to provide them. Just use them if you want to change some settings. The description of the meaning of given setting, you can find below.

> [!SETTINGS]- [enabled](#+obsidian.callouts.enabled){#+obsidian.callouts.enabled}
> Control if callouts are generated on the document web page.

> [!SETTINGS]- [indentation](#+obsidian.callouts.indentation){#+obsidian.callouts.indentation}
> Defines if callout indentation whitespace type. Possible values: `spaces` (default) or `tabs`.

### Links

===+ ":octicons-file-code-16: mkdocs.yml"

``` yaml hl_lines="3-5"
plugins:
  - pub-obsidian:
	links:
	  wikilinks_enabled: true
	  img_lazy: true
```

Above you can find all possible settings with their default values. You don't have to provide them. Just use them if you want to change some settings. The description of the meaning of given setting, you can find below.

> [!SETTINGS]- [wikilinks_enabled](#+obsidian.links.wikilinks_enabled){#+obsidian.links.wikilinks_enabled}
> Control if WikiLinks format is supported.

> [!SETTINGS]- [img_lazy](#+obsidian.links.img_lazy){#+obsidian.links.img_lazy}
> Controls if all images should be [lazy loaded](https://developer.mozilla.org/en-US/docs/Web/Performance/Lazy_loading). By default, this setting is enabled because it helps with SEO. However, you can disable this option and [add set it up for each image separately](https://squidfunk.github.io/mkdocs-material/reference/images/?h=image#image-lazy-loading).

### Vega charts

===+ ":octicons-file-code-16: mkdocs.yml"

``` yaml hl_lines="3-6"
plugins:
  - pub-obsidian:
	vega:
	  enabled: true
	  vega_schema: https://vega.github.io/schema/vega/v5.json
	  vega_lite_schema: https://vega.github.io/schema/vega-lite/v5.json
```

Above you can find all possible settings with their default values. You don't have to provide them. Just use them if you want to change some settings. The description of the meaning of given setting, you can find below.

> [!SETTINGS]- [enabled](#+obsidian.vega.enabled){#+obsidian.vega.enabled}
> Controls if Vega charts are supported and will be rendered.

> [!SETTINGS]- [vega_schema](#+obsidian.vega.vega_schema){#+obsidian.vega.vega_schema}
> Link to JSON file with Vega scheme.

> [!SETTINGS]- [vega_lite_schema](#+obsidian.vega.vega_lite_schema){#+obsidian.vega.vega_lite_schema}
> Link to JSON file with Vega-lite scheme.
