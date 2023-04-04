---
title: Setting up social cards
slug: setting-up-social-cards
status: published
date: 2023-04-04 21:14:00
update: 2023-04-04 23:03:49
categories: setup plugin social cards
description: Setting up social cards plugin
---

# Setting up social cards plugin

When you are a blogger or a person who wants to publish some documentation, book or any other piece of written text, you probably also want to share it over social media. Most platforms (like Facebook, LinkedIn, etc.) uses some web page metadata called [Open Graph](https://ogp.me). Twitter is using part of this data and some additional metadata called [Twitter Cards](https://developer.twitter.com/en/docs/twitter-for-websites/cards/overview/abouts-cards). No matter if you want to share your text with Facebook or Twitter, MkDocs Publisher is here to help you with this task and is doing it (almost) fully automatically. You don't have to edit any template like it's needed when you would like to use similar functionality from [Material for MkDosc](https://squidfunk.github.io/mkdocs-material/setup/setting-up-social-cards/?h=social) theme (at least it's true for `v9.1.5`). At this time (MkDocs Publisher `v0.5.0`) it's not possible to auto-generate a whole social card (this task is added to the [backlog](../05_dev/01_backlog.md)). However, it's possible to add your image as a preview with additional description, etc.

## Document metadata

Markdown documents can contain additional metadata that is not rendered by MkDocs. This metadata is located at the beginning of the file (more information about this you can found in MkDocs documentation in [Meta-Data section](https://www.mkdocs.org/user-guide/writing-your-docs/#meta-data)).

Some data used by social cards is global (like site name) but some are unique per document. Data needed and optional that is needed by social card is:

-  (required)`title` - document title (30–65 characters),
-  (required) `description` - short document description (120–350 characters),
-  (optional) `image` - link to an image (1200×630 pixels).

===+ "YAML Style Meta-Data"

	It's prefered style since more plugins supports it.

	```markdown
	---
	title: Your document title
	description: A short description of document content that encourage to read it
	image: /some/url/to/an/image.jpg
	---

	This is the first paragraph of the document.
	```

=== "MultiMarkdown Style Meta-Data"

	This style is NOT prefered since not all plugins supports it.

	```markdown
	Title: Your document title
	Description: A short description of document content that encourage to read it
	Image: /some/url/to/an/image.jpg

	This is the first paragraph of the document.
	```

!!! warning

	If any of the required key is missing, social card will not be included in a web page.

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

[enabled](#+social.og.enable){ #+social.og.enable }

:   :octicons-milestone-16: Default: `true` - this option gives you an ability to enable or disable an Open Graph cards:

    ===+ ":octicons-file-code-16: mkdocs.yml"

        ```yaml hl_lines="3-4"
        plugins:
          - pub-social:
	          og:
	            enabled: true
        ```

[locale](#+social.og.locale){ #+social.og.locale }

:   :octicons-milestone-16: Default: `en_US` - this option gives you an ability to set a locale of an Open Graph cards:

    ===+ ":octicons-file-code-16: mkdocs.yml"

        ```yaml hl_lines="3-4"
        plugins:
          - pub-social:
	          og:
	            locale: en_us
        ```

	There is a limited set of [possible values](https://developer.yoast.com/features/opengraph/api/changing-og-locale-output/).

#### Twitter cards

[enabled](#+social.twitter.enable){ #+social.twitter.enable }

:   :octicons-milestone-16: Default: `true` - this option gives you an ability to enable or disable a Twitter Cards:

    ===+ ":octicons-file-code-16: mkdocs.yml"

        ```yaml hl_lines="3-4"
        plugins:
          - pub-social:
	          twitter:
	            enabled: true
        ```

[website](#+social.twitter.website){ #+social.twitter.website }

:   :octicons-milestone-16: Default: `''` - this option gives you an ability to add a Twitter [website account](https://business.twitter.com/en/basics/create-a-twitter-business-profile.html) name:

    ===+ ":octicons-file-code-16: mkdocs.yml"

        ```yaml hl_lines="3-4"
        plugins:
          - pub-social:
	          twitter:
	            website: @website
        ```

[author](#+social.twitter.author){ #+social.twitter.author }

:   :octicons-milestone-16: Default: `''` - this option gives you an ability to add a Twitter [author account](https://help.twitter.com/en/using-twitter/create-twitter-account) name:

    ===+ ":octicons-file-code-16: mkdocs.yml"

        ```yaml hl_lines="3-4"
        plugins:
          - pub-social:
	          twitter:
	            author: @author
        ```

#### Metadata keys names

You can change a name of the keys used to store metadata used to create social cards.

[title_key](#+social.meta_keys.title_key){ #+social.meta_keys.title_key }

:   :octicons-milestone-16: Default: `title` - this option gives you an ability to change a metadata title key used to create a social card:

    ===+ ":octicons-file-code-16: mkdocs.yml"

        ```yaml hl_lines="3-4"
        plugins:
          - pub-social:
	          meta_keys:
	             title_key: title
        ```

[description_key](#+social.meta_keys.description_key){ #+social.meta_keys.description_key }

:   :octicons-milestone-16: Default: `description` - this option gives you an ability to change a metadata description key used to create a social card:

    ===+ ":octicons-file-code-16: mkdocs.yml"

        ```yaml hl_lines="3-4"
        plugins:
          - pub-social:
	          meta_keys:
	             description_key: description
        ```

[image_key](#+social.meta_keys.image_key){ #+social.meta_keys.image_key }

:   :octicons-milestone-16: Default: `title` - this option gives you an ability to change a metadata image key used to create a social card:

    ===+ ":octicons-file-code-16: mkdocs.yml"

        ```yaml hl_lines="3-4"
        plugins:
          - pub-social:
	          meta_keys:
	             image_key: image
        ```
