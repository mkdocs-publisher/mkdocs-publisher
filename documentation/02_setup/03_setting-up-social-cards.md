---
title: Setting up social cards
slug: pub-social
status: published
date: 2023-04-04 21:14:00
update: 2023-06-09 12:01:11
description: Setting up social cards plugin
categories: setup plugin social cards
---

# Setting up social cards plugin

When you are a blogger or a person who wants to publish some documentation, book or any other piece of written text, you probably also want to share it over social media. Most platforms (like Facebook, LinkedIn, etc.) uses some web page metadata called [Open Graph](https://ogp.me). Twitter is using part of this data and some additional metadata called [Twitter Cards](https://developer.twitter.com/en/docs/twitter-for-websites/cards/overview/abouts-cards). No matter if you want to share your text with Facebook or Twitter, MkDocs Publisher is here to help you with this task and is doing it (almost) fully automatically. You don't have to edit any template like it's needed when you would like to use similar functionality from [Material for MkDosc](https://squidfunk.github.io/mkdocs-material/setup/setting-up-social-cards/?h=social) theme (at least it's true for `v9.1.5`). At this time (MkDocs Publisher `v0.5.0`) it's not possible to auto-generate a whole social card (this task is added to the [backlog](../05_dev/other/02_backlog.md)). However, it's possible to add your image as a preview with additional description, etc.

## Document metadata

More about document metadata you can read in the document related to setting up the [meta plugin](02_setting-up-meta.md#document-metadata).

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

### Enable social cards

To enable the built-in social cards plugin, the following lines have to be added to `mkdocs.yml` file:

===+ ":octicons-file-code-16: mkdocs.yml"

    ```yaml hl_lines="2"
    plugins:
      - pub-social
    ```

### Settings

#### Open Graph cards

> [!SETTINGS]+ [enabled](#+social.og.enable){ #+social.og.enable } (default: `true`)
> This option gives you an ability to enable or disable an Open Graph cards:

    ===+ ":octicons-file-code-16: mkdocs.yml"

        ```yaml hl_lines="3-4"
        plugins:
          - pub-social:
	          og:
	            enabled: true
        ```

> [!SETTINGS]+ [locale](#+social.og.locale){ #+social.og.locale } (default: `en_US`)
> This option gives you an ability to set a locale of an Open Graph cards:

    ===+ ":octicons-file-code-16: mkdocs.yml"

        ```yaml hl_lines="3-4"
        plugins:
          - pub-social:
	          og:
	            locale: en_us
        ```

	There is a limited set of [possible values](https://developer.yoast.com/features/opengraph/api/changing-og-locale-output/).

#### Twitter cards

> [!SETTINGS]+ [enabled](#+social.twitter.enable){ #+social.twitter.enable } (default: `true`)
> This option gives you an ability to enable or disable a Twitter Cards:

    ===+ ":octicons-file-code-16: mkdocs.yml"

        ```yaml hl_lines="3-4"
        plugins:
          - pub-social:
	          twitter:
	            enabled: true
        ```

> [!SETTINGS]+ [website](#+social.twitter.website){ #+social.twitter.website } (default: `''`)
> This option gives you an ability to add a Twitter [website account](https://business.twitter.com/en/basics/create-a-twitter-business-profile.html) name:

    ===+ ":octicons-file-code-16: mkdocs.yml"

        ```yaml hl_lines="3-4"
        plugins:
          - pub-social:
	          twitter:
	            website: @website
        ```

> [!SETTINGS]+ [author](#+social.twitter.author){ #+social.twitter.author }(default: `''`)
> This option gives you an ability to add a Twitter [author account](https://help.twitter.com/en/using-twitter/create-twitter-account) name:

    ===+ ":octicons-file-code-16: mkdocs.yml"

        ```yaml hl_lines="3-4"
        plugins:
          - pub-social:
	          twitter:
	            author: @author
        ```

#### Metadata keys names

You can change a name of the keys used to store metadata used to create social cards.

> [!SETTINGS]+ [title_key](#+social.meta_keys.title_key){ #+social.meta_keys.title_key } (default: `title`)
> This option gives you an ability to change a metadata title key used to create a social card:

    ===+ ":octicons-file-code-16: mkdocs.yml"

        ```yaml hl_lines="3-4"
        plugins:
          - pub-social:
	          meta_keys:
	             title_key: title
        ```

> [!SETTINGS]+ [description_key](#+social.meta_keys.description_key){ #+social.meta_keys.description_key } (default: `description`)
> This option gives you an ability to change a metadata description key used to create a social card:

    ===+ ":octicons-file-code-16: mkdocs.yml"

        ```yaml hl_lines="3-4"
        plugins:
          - pub-social:
	          meta_keys:
	             description_key: description
        ```

> [!SETTINGS]+ [image_key](#+social.meta_keys.image_key){ #+social.meta_keys.image_key } (default: `image`)
> This option gives you an ability to change a metadata image key used to create a social card:

    ===+ ":octicons-file-code-16: mkdocs.yml"

        ```yaml hl_lines="3-4"
        plugins:
          - pub-social:
	          meta_keys:
	             image_key: image
        ```
