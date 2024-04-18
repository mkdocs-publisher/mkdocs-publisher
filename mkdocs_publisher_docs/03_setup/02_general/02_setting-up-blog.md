---
title: Setting up a blog
icon: material/newspaper-variant-multiple
slug: pub-blog
publish: true
date: 2023-02-12 22:00:00
update: 2023-10-03 12:27:41
description: Setting up a Publisher for MkDocs blog plugin for blogging functionality
categories:
  - setup
  - plugin
  - blog
---

# Setting up a blog plugin

## Introduction

**Publisher for MkDocs** allows you to create a blog. A blog can be a sidecar for your current documentation, or it can be configured as a standalone. The entire blogging engine is created and preconfigured, so you can focus on content creation. It will handle creation of:

- indexes,
- archive,
- categories,
- tags,
- pagination.

All the above documents are created outside `docs` directory, so they are not visible and do not interfere with your content.

This documentation contains a [blog](../../../blog/) that is created using this plugin, so you can take a look at a living example.


> [!TIP] Date format
> Currently, the date format of a blog posts is not configurable and has to look like this:
> ``` yaml
> ---
> date: 2023-02-12 22:00:00
> ---
> ```
> There is also a requirement, that each blog post, have to contain an unique date because without this, the algorithm responsible for posts display ordering (from newest to oldest) will not work correctly.

## Configuration

To enable the built-in obsidian blog, the following lines have to be added to `mkdocs.yml` file:

===+ ":octicons-file-code-16: mkdocs.yml"

    ```yaml hl_lines="2"
    plugins:
      - pub-blog
    ```

=== ":fontawesome-solid-folder-tree:"

    By default, the blogging plugin assumes that blog posts are located inside `blog` subdirectory. You have to create this directory manually, so the directory structure will look like this:

    ```console hl_lines="3"
    .
    ├─ docs/
    │  └─ blog/
    └─ mkdocs.yml
    ```

The last thing is to add a blog to a site navigation. There are 2 ways to do it:

=== "Using _pub-meta_ plugin"

	When [pub-meta](01_setting-up-meta.md) plugin is configured and the directory for blog posts is set up, there is nothing more left to be configured. All the things related to creating a navigation section will be handled automatically by the _pub-meta_ plugin.

=== "Add to existing site layout"

	If an existing pages are created in MkDocs, it's simple to just add a blog functionality. To achieve it, _Any name_ with path to a blog subdirectory name (by default it's a `blog`) has to be added to the `mkdocs.yml` file and blogging engine will handle everything else.

    === ":octicons-file-code-16: mkdocs.yml"

        ```yaml hl_lines="3"
        nav:
          - ... # Previous navigation elements
          - Any name: blog
          - ... # Next navigation elements
        ```


> [!INFO] Blog standalone mode
> Standalone mode (blog as a starting page) was removed in version [v0.6.0](../../06_blog/v100-obsidian.md) and now this is automatically detected, based on site navigation structure.

### General

===+ ":octicons-file-code-16: mkdocs.yml"

	```yaml hl_lines="3-6"
	plugins:
	  - pub-blog:
		  teaser_marker: "<!-- more -->"
		  searchable_non_posts: false
		  posts_per_page: 5
		  slug: blog
	```

Above you can find all possible settings with their default values. You don't have to provide them. Just use them if you want to change some settings. The description of the meaning of given setting, you can find below.

> [!SETTINGS]- [teaser_marker](#+blog.teaser_marker){#+blog.teaser_marker}
> This option gives you an ability to split a blog posts that are a massive chunk of text into two parts: blog post teaser visible on blog posts index page and the full article. To split the blog post, you have to put a `<!-- more -->` in some line inside a content of your blog post. This value is a valid HTML comment, so it will not be rendered.

> [!SETTINGS]- [posts_per_page](#+blog.posts_per_page){#+blog.posts_per_page}
> When you gather over time some amount of blog posts, their index even with short teasers, they can take quite much space over a single page and scrolling down is not a convenient solution. To avoid this, blogging engine allows splitting index pages when they contain a certain amount of blog posts.

> [!SETTINGS]- [searchable_non_posts](#+blog.searchable_non_posts){#+blog.searchable_non_posts}
> This option controls the behavior of [a search plugin](https://squidfunk.github.io/mkdocs-material/setup/setting-up-site-search/) for all dynamically created blog documents that are not blog posts. There is no need to make those pages visible, since all the text in those pages is a copy of the part of the blog post.

> [!SETTINGS]- [slug](#+blog.slug){#+blog.slug}
> This option gives you an ability to go to specify your blog direct URL, like `https://yourblog.com/blog/`. The `blog` part of the URL can be configured to a non-standard value.

### Directories

This plugin to work correctly, needs to create and/or use some directories. Those settings should be considered as advanced and for day to day use, you should not change them.

===+ ":octicons-file-code-16: mkdocs.yml"

	``` yaml hl_lines="3-6"
	plugins:
	  - pub-blog:
		  temp_dir: .pub_blog_temp
		  archive_subdir: archive
		  categories_subdir: categories
		  tags_subdir: tags
	```

=== ":fontawesome-solid-folder-tree:"

	Temporary directory is created at the same level as main `docs` directory and `mkdocs.yml` configuration file.

	```console hl_lines="2-5"
	.
	├─ .pub_blog_temp/
	│  ├─ archive/
	│  ├─ categories/
	│  └─ tags/
	├─ docs/
	│  └─ blog/
	└─ mkdocs.yml
	```

> [!SETTINGS]- [temp_dir](#+blog.temp_dir){#+blog.temp_dir}
> Temporary directory is used by a blog engine to create an index files with a blog post teasers and other files like a list of archive, categories, and tags pages.

> [!SETTINGS]- [archive_subdir](#+blog.archive_subdir){#+blog.archive_subdir}
> Archive subdirectory is used to store dynamically generated documents that contain archive indexes.

> [!SETTINGS]- [categories_subdir](#+blog.categories_subdir){#+blog.categories_subdir}
> Categories subdirectory is used to store dynamically generated documents that contain categories indexes.

> [!SETTINGS]- [tags](#+blog.tags){#+blog.tags }
> Tags subdirectory is used to store dynamically generated documents that contain tags indexes.

### Language

By default, the blogging plugin is set to use _English_ (`en`) translation. Currently, available languages:

- `en` - English,
- `pl` - Polish.

To set up one of the above languages, the following line has to be added to the `mkdocs.yml` file:

===+ ":octicons-file-code-16: mkdocs.yml"

```yaml hl_lines="3"
plugin:
  - pub-blog:
      lang: "pl"
```

#### Translation

If there is no language that suits you best, you can translate part of the interface by providing values for the below keys inside the configuration `mkdocs.yml` files. Providing those values overrides values for setup of a given language, and this way it's possible to change only some of them.

Below, you can find a list of settings keys with English values that allow to translate some parts of the interface:

===+ ":octicons-file-code-16: mkdocs.yml"

```yaml hl_lines="3-15"
plugins:
  pub-blog:
    translation:
      teaser_link_text: Read more
      blog_page_title: Blog
      blog_navigation_name: Blog
      recent_blog_posts_navigation_name: Recent posts
      archive_page_title: Archive
      archive_navigation_name: Archive
      categories_page_title: Category
      categories_navigation_name: Categories
      tags_page_title: Tag
      tags_navigation_name: Tags
      newer_posts: Newer posts
      older_posts: Older posts
```
