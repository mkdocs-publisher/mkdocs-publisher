---
title: Setting up social cards
icon: material/share
slug: pub-social
publish: true
date: 2023-04-04 21:14:00
update: 2024-06-12 17:37:54
description: Setting up Publisher for MkDocs social cards plugin for social services sharing
categories:
  - setup
  - plugin
  - social cards
---

# Setting up social cards plugin

## Introduction

When you are a blogger or a person who wants to publish some documentation, book or any other piece of written text, you probably also want to share it over social media. Most platforms (like Facebook, LinkedIn, etc.) uses some web page metadata called [Open Graph](https://ogp.me). Twitter is using part of this data and some additional metadata called [Twitter Cards](https://developer.twitter.com/en/docs/twitter-for-websites/cards/overview/abouts-cards). No matter if you want to share your text with Facebook or Twitter, MkDocs Publisher is here to help you with this task and is doing it (almost) fully automatically. You don't have to edit any template like it's needed when you would like to use similar functionality from [Material for MkDosc](https://squidfunk.github.io/mkdocs-material/setup/setting-up-social-cards/?h=social) theme (at least it's true for `v9.1.5`). At this time (MkDocs Publisher `v0.5.0`) it's not possible to auto-generate a whole social card (this task is added to the [backlog](../../07_dev/other/02_backlog.md)). However, it's possible to add your image as a preview with additional description, etc.

## Document metadata

More about document metadata you can read in the document related to setting up the [meta plugin](../02_general/01_setting-up-meta.md#Document%20meta-data).


Some data used by social cards is global (like site name) but some are unique per document. Data needed and optional that is needed by social card is:

-  (required)`title` - document title (30–65 characters),
-  (required) `description` - short document description (120–350 characters),
-  (optional) `image` - link to an image (1200×630 pixels).

===+ ":octicons-markdown-16: example.md"

	```yaml hl_lines="2-4"
	---
	title: Your document title
	description: A short description of document content that encourage to read it
	image: /some/url/to/an/image.jpg
	---
	```

>  [!WARNING]
> If any of the required key is missing, social card will not be included in a web page.

## Configuration

To enable the built-in social cards plugin, the following lines have to be added to `mkdocs.yml` file:

===+ ":octicons-file-code-16: mkdocs.yml"

    ```yaml hl_lines="2"
    plugins:
      - pub-social
    ```

### Open Graph cards

===+ ":octicons-file-code-16: mkdocs.yml"

	```yaml hl_lines="3-5"
	plugins:
	  - pub-social:
		  og:
			enabled: true
			locale: en_us
	```

> [!SETTINGS]- [enabled](#+social.og.enable){#+social.og.enable}
> This option gives you an ability to enable or disable an Open Graph cards.

> [!SETTINGS]- [locale](#+social.og.locale){#+social.og.locale}
> This option gives you an ability to set a locale of an Open Graph cards. There is a limited set of [possible values](https://developer.yoast.com/features/opengraph/api/changing-og-locale-output/).

### Twitter cards

===+ ":octicons-file-code-16: mkdocs.yml"

	```yaml hl_lines="3-6"
	plugins:
	  - pub-social:
		  twitter:
			enabled: true
			website: @website
			author: @author
	```

> [!SETTINGS]- [enabled](#+social.twitter.enable){#+social.twitter.enable}
> This option gives you an ability to enable or disable a Twitter Cards.

> [!SETTINGS]- [website](#+social.twitter.website){#+social.twitter.website}
> This option gives you an ability to add a Twitter [website account](https://business.twitter.com/en/basics/create-a-twitter-business-profile.html) name.

> [!SETTINGS]- [author](#+social.twitter.author){#+social.twitter.author}
> This option gives you an ability to add a Twitter [author account](https://help.twitter.com/en/using-twitter/create-twitter-account) name.

### Metadata keys names

You can change a name of the keys used to store metadata used to create social cards.

===+ ":octicons-file-code-16: mkdocs.yml"

	```yaml hl_lines="3-6"
	plugins:
	  - pub-social:
		  meta_keys:
			 title_key: title
			 description_key: description
			 image_key: image
	```

> [!SETTINGS]- [title_key](#+social.meta_keys.title_key){#+social.meta_keys.title_key}
> This option gives you an ability to change a metadata title key used to create a social card.

> [!SETTINGS]- [description_key](#+social.meta_keys.description_key){#+social.meta_keys.description_key}
> This option gives you an ability to change a metadata description key used to create a social card.

> [!SETTINGS]- [image_key](#+social.meta_keys.image_key){#+social.meta_keys.image_key}
> This option gives you an ability to change a metadata image key used to create a social card.
