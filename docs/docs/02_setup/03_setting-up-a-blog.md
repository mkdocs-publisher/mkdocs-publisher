---
title: Setting up a blog
slug: setting-up-a-blog
status: published
date: 2023-02-12 22:00:00
update: 2023-03-17 23:09:54
categories: setup plugin blog
description: Setting up blog plugin
---

# Setting up a blog plugin

Publisher for MkDocs allows you to create a blog. A blog can be a sidecar for your current documentation, or it can be configured as a standalone. The entire blogging engine is created and preconfigured, so you can focus on content creation. It will handle creation of:

- indexes,
- archive,
- categories,
- tags,
- pagination.

All the above documents are created outside `docs` directory, so they are not visible and do not interfere with your content.

This documentation contains a [blog](../blog/) that is created using this plugin, so you can take a look at a living example.

## Basic configuration

To enable the built-in blog plugin, the following lines have to be added to `mkdocs.yml` file:

```yaml title="mkdocs.yml"
plugins:
  - pub-blog
```

By default, the blogging plugin assumes that blog posts are located inside `blog` subdirectory. You have to create this directory manually, so the directory structure will look like this:

```bash
.
├─ docs/
│  └─ blog/ # (1)!
└─ mkdocs.yml
```

1. This is a directory where to create a blog posts

The last thing is to add a blog to a site navigation. There are 3 ways to do it:

=== "Add to existing site layout"

    If an existing pages are created in MkDocs, it's simple to just add a blog functionality. To achieve it, _Any name_ with path to a blog subdirectory name (by default it's a `blog`) has to be added to the `mkdocs.yml` file and blogging engine will handle everything else.

    ```yaml title="mkdocs.yml"
    nav:
      - ... # (1)!
      - Any name: blog # (2)!
      - ... # (3)!
    ```

    1. Previous navigation configuration keys
    2. Navigation to a `blog` directory with an _Any name_
    3. Rest of the navigation configuration keys

=== "Using _pub-auto-nav_ plugin"

    When [pub-auto-nav](02_setting-up-auto-nav.md) plugin is configured and directory for blog posts is set up, there is nothing more left to be configured. All the things related to creating navigation section will be handled automatically by the _pub-auto-nav_ plugin.

=== "Standalone mode"

    A standalone mode gives a posibility to setup a MkDocs for just a pure blogging experience. Blog will become a main page. To make it happen, the following lines have to be added to `mkdocs.yml` file:

    ```yaml title="mkdocs.yaml"
    plugins:
      pub-blog:
        start_page: true # (1)!
    ```

    1. This enables a standalone mode

    Documents created outisde directory where blog posts are stored, will be considered as out of navigation configuration but still rendred. To use them, you have to put links to them inside blog posts or by editing thame template files.

---

## Advanced settings

### Slug

When using non-standalone blog mode, it's good to have an ability to go to your blog by a direct URL, like `https://yourblog.com/blog/`. The `blog` part of the URL can be configured to a non-standard value:

```yaml title="mkdocs.yml"
plugins:
  - pub-blog:
      slug: blog # (1)!
```

1. The default value for slug.

### Teaser marker

Usually, blog posts are a huge chunk of text. Putting a longer text on an index page, can be not convenient for your blog audience. To split a longer blog post into a teaser part and a full article, you have to put a `<!-- more -->` in some line inside a content of your blog post. This value is a valid HTML comment, so it will not be rendered. If for any reason, you need to change it, you can do it by adding the following configuration key:

```yaml title="mkdocs.yml"
plugins:
  - pub-blog:
      teaser_marker: `<!-- more -->` # (1)!
```

1. The default value for teaser marker.

### Pagination

When you gather over time some amount of blog posts, their index even with short teasers, they can take quite much space over a single page and scrolling down is not a convenient solution. To avoid this, blogging engine allows splitting index pages when they contain a certain amount of blog posts.  By default, it's set to 5, but you can change it by adding a following configuration key:

```yaml title="mkdocs.yml"
plugins:
  - pub-blog:
      posts_per_page: 5 # (1)!
```

1. The default value for the number of posts per page.

### Directories

This plugin to work correctly, needs to create and/or use some directories. Those settings should be considered as advanced and for day to day use, you should not change them.


=== "`temp_dir`"

    Temporary directory is used by a blog engine to create an index files with a blog post teasers and other files like a list of archive, categories and tags pages.

    ``` yaml title="mkdocs.yml"
    plugins:
      - pub-blog:
          temp_dir: .temp # (1)!
    ```

    1. The default value.

    Temporary directory is created at the same level as main `docs` directory and `mkdocs.yml` configuration file.

    ```bash
    .
    ├─ .temp/
    ├─ docs/
    │  └─ blog/
    └─ mkdocs.yml
    ```

=== "`archive_subdir`"

    Archive directory is used to store dynamically generated documents that contains archive indexes.

    Some description

    ``` yaml title="mkdocs.yml"
    plugins:
      - pub-blog:
          archive_subdir: archive # (1)!
    ```

    1. The default value.

    Archive directory is a subdirectory to a temporary directory.

    ```bash
    .
    ├─ .temp/
    │  └─ archive/ # (1)!
    ├─ docs/
    │  └─ blog/
    └─ mkdocs.yml
    ```

    1. The default value.

=== "`categories_subdir`"

    Categories directory is used to store dynamically generated documents that contains categories indexes.

    ``` yaml title="mkdocs.yml"
    plugins:
      - pub-blog:
          categories_subdir: categories # (1)!
    ```

    1. The default value.

    Categories directory is a subdirectory to a temporary directory.

    ```bash
    .
    ├─ .temp/
    │  └─ categories/ # (1)!
    ├─ docs/
    │  └─ blog/
    └─ mkdocs.yml
    ```

    1. The default value.

=== "`tags_subdir`"

    Tags directory is used to store dynamically generated documents that contains tags indexes.

    ``` yaml title="mkdocs.yml"
    plugins:
      - pub-blog:
          tags_subdir: tags # (1)!
    ```

    1. The default value.

    Tags directory is a subdirectory to a temporary directory.

    ```bash
    .
    ├─ .temp/
    │  └─ tags/ # (1)!
    ├─ docs/
    │  └─ blog/
    └─ mkdocs.yml
    ```

    1. The default value.

---

### Language

By default, the blogging plugin is set to use _English_ (`en`) translation. Currently, available languages:

- `en` - English,
- `pl` - Polish.

To set up one of the above languages, the following line has to be added to the `mkdocs.yml` file:

```yaml title="mkdosc.yml"
plugin:
  - pub-blog:
      lang: 'pl' # (1)!
```

1. Set language to Polish

#### Translation

If there is no language that suits you best, you can translate part of the interface by providing values for the below keys inside the configuration `mkdocs.yml` files. Providing those values overrides values for setup of a given language, and this way it's possible to change only some of them.

Below, you can find a list of settings keys with English values that allow to translate some parts of the interface:

```yaml title="mkdocs.yaml"
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
