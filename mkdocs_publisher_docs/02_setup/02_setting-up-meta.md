---
title: Setting up meta
slug: pub-meta
status: published
date: 2023-05-15 16:00:00
update: 2023-08-01 11:51:58
description: Setting up Publisher for MkDocs meta plugin for metadata retrival and automatic navigation building
categories:
  - setup
  - plugin
  - meta
---

# Setting up the meta plugin

## Introduction

As you can see on the left - side menu, this plugin is placed as the first one. It is because this plugin can be considered as one that influences the way, you will be writing a documentation. So, why it's so essential?

There are a few reasons:

1. Automatic navigation building based on file and directory names. This simplifies a process of a document navigation creation in `mkdocs.yml` file, described in [official documentation](https://www.mkdocs.org/user-guide/writing-your-docs/#configure-pages-and-navigation).
2. Based on file meta-data, you can set document:
	- [URL](#Navigation%20automatic%20generation).
	- [creation/update date](#Dates).
	- [document publication state](#Document%20publication%20status)
	- and some other less important.
	Most of these options, influence the SEO of the page build using MkDocs.

Probably you are now wondering why 2 quite different functionalities are placed in one plugin?

The answer is not so obvious and a bit technical, but in bigger simplification, it's way simpler and less complex to bound those functionalities together. The main reason for that is how MkDocs internals work. For example, when navigation is built and when final HTML files are generated. Other example could be a document status implementation that influences navigation building, file list creation and `sitemap.xml` creation. This process should be considered as one functionality and splitting it over 2 separate plugins is possible, but it will not only increase code complexity, but also will increase significantly complexity of configuration since many settings used for automatic navigation building are the same for defining file meta-data. So, if we split functionality into 2 separate plugins, the final user (You) will have to maintain consistency in `mkdocs.yml` file. With a single plugin approach, we can reduce this problem to just maintaining a single point of configuration and settings validation.

> [!warning] Important information
> However, this plugin is not needed for other plugins to work correctly, it's highly recommended to use it.

## Meta-data

Markdown documents can contain additional metadata that is not rendered by MkDocs. This metadata is located at the beginning of the file (more information about this you can found in MkDocs documentation in [Meta-Data section](https://www.mkdocs.org/user-guide/writing-your-docs/#meta-data)).

MkDocs supports 2 main formats of meta-data:

===+ ":octicons-markdown-16: YAML_style.md"

	It's preferred style since more plugins supports it and its the same format as in `mkdocs.yml` file. Also this format is supported by other tools (like [Jekyll](https://jekyllrb.com/docs/front-matter/) that is used in GitHub or [GitLab](https://docs.gitlab.com/ee/user/markdown.html#front-matter))

	```markdown
	---
	title: Your document title
	description: A short description of document content that encourage to read it
	---

	This is the first paragraph of the document.
	```

=== ":octicons-markdown-16: MultiMarkdown_syle.md"

	This style is NOT prefered since not all plugins and other tools supports it.

	```markdown
	Title: Your document title
	Description: A short description of document content that encourage to read it

	This is the first paragraph of the document.
	```

> [!info] YAML front matter
> Since the YAML front matter format for meta-data is used by a wider set of other plugins and tools, this format will be used in this tool documentation.

### Document meta-data

As described in the previous section, you can provide additional meta-data that is unique for that document, and can change some behavior of the meta plugin, but not only. Some other MkDocs plugins also utilize these types of settings. One of the plugins is [pub-blog](04_setting-up-blog.md) or [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/).

### Directory meta-data

The same approach can be taken for setting this up in the case of directories. To provide meta-data values, you have to create a file `README.md` inside the given directory and put the values accepted by this plugin. A list of possible settings can be found below.

## Dates

In the metadata, there is a possibility to add two values related to dates.

=== ":material-calendar-month: `date`"

	This defines a value for the document's creation date. It's also used by [a blog plugin](04_setting-up-blog.md) for blog posts ordering and a meta plugin for updating a sitemap file.

	```yaml hl_lines="2"
	---
	date: 2023-05-19 15:40:36
	---
	```

=== ":material-calendar-month: `update`"

	This defines a value for the document's last update date. It's also used by a meta plugin for updating a sitemap file.

	```yaml hl_lines="2"
	---
	update: 2023-06-12 14:16:52
	---
	```

> [!Info] Date format
> Currently, the date format is hard-coded and cannot be changed, and is defined according to [Python date format codes](https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes) and looks like this: `%Y-%m-%d %H:%M:%S` (example: `2023-06-12 14:16:52`).


## Navigation automatic generation

> [!warning] Warning
> If the meta plugin is enabled, document navigation is automatically created by the plugin. So if you have your navigation already created, you will have to set up the navigation in the way, how meta plugin is building it. Currently, this is the only way to provide functionality like single document or directories status.

In short, navigation automatic generation works based on alphabetical order of files and directories. If you are using any IDE (like [PyCharm](https://www.jetbrains.com/pycharm/), [VsCode](https://code.visualstudio.com) or [Obsidian](https://obsidian.md)) for documents creation and editing, the way of file order you see by default in the project or file browser of the tool, is the order of the files in navigation. Probably the easiest way of file ordering is to provide some prefix with the digits (take a look at [this documentation repository](https://github.com/mkusz/mkdocs-publisher/tree/main/documentation) for better understanding). The main problem with this approach would be strange names in file URLs and documentation titles on the web page. To solve that problems, the meta plugin uses two meta-data values that are common for document files and directories:

===+ "`title`"

	`title` is responsible for document name that is visible in the generated web page.

	```yaml hl_lines="2"
	---
	title: Document title
	---
	```

=== "`slug`"

	`slug` is responsible for document URL.

	```yaml hl_lines="2"
	---
	slug: document-slug
	---
	```

### Document publication status

One of the functions provided by the meta plugin is a possibility to set document status. Each status has some implications for navigation building and links creation.

===+ ":octicons-markdown-16: published.md"

	```yaml hl_lines="2"
	---
	status: published
	---
	```

	When the document status is set to `published`, the document will appear in navigation and link to it, will be visible on the generated web page.

=== ":octicons-markdown-16: hidden.md"

	```yaml hl_lines="2"
	---
	status: hidden
	---
	```

	When the document status is set to `hidden`, the document will not appear in navigation, but will be generated, and it's possible to create a link to this document or enter a direct URL address.

=== ":octicons-markdown-16: draft.md"

	```yaml hl_lines="2"
	---
	status: draft
	---
	```

	When the document status is set to `draft`, the document will not appear in navigation and will not be generated. However, when using local document hosting by issuing the command `mkdocs serve`, each draft document will be generated to help with document creation and visual inspection.

> [!NOTE] Default document status
> If status is not set for document, by default status is set to `draft`, so the document will not be published accidentally.

### Directory publication status

Status can also be set for whole directories. This gives you a control over the whole set of documents that are placed in given directories. Each status has some implications for navigation building and links creation.

===+ ":octicons-markdown-16: README.md for published directory"

	```markdown hl_lines="2"
	---
	status: published
	---
	```

	When the status is set to `published` in `README.md` file, the directory will appear in navigation and link to it and documents in this directory, will be visible on the generated web page.

=== ":octicons-markdown-16: README.md for draft directory"

	```markdown hl_lines="2"
	---
	status: draft
	---
	```

	When the status is set to `draft` in `README.md` file, the directory will not appear in navigation and documents in this directory will not be generated. However, when using local document hosting by issuing the command `mkdocs serve`, each directory and documents will be generated to help with document creation and visual inspection.

> [!NOTE] Default directory status
> If status is not set for directory, by default status is set to `published`, so there is no need to create `README.md` file in each directory.

## Configuration

### Enable meta plugin

To enable the built-in meta plugin, the following lines have to be added to `mkdocs.yml` file:

===+ ":octicons-file-code-16: mkdocs.yml"

    ```yaml hl_lines="2"
    plugins:
      - pub-meta
    ```

### Settings

> [!SETTINGS]+ [dir_meta_file](#+meta.dir_meta_file){ #+meta.dir_meta_file } (default: `README.md`)
> File name containing metadata for directories. The default file name is `README.md` because this file name is used by [GitHub](https://docs.github.com/articles/about-readmes) and [GitLab](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes) (the two most popular git repositories providers) as an index files for the directory. By using this name, this file ideally blends into git repository when the whole documentation is stored in one.

    ===+ ":octicons-file-code-16: mkdocs.yml"

        ```yaml hl_lines="3"
        plugins:
          - pub-meta:
	          dir_meta_file: README.md
        ```

#### Slug

> [!SETTINGS]+ [enabled](#+meta.slug.enabled){ #+meta.slug.enabled } (default: `true`)
> Control if slug metadata will be used while document URL is created while generating a web page.

    ===+ ":octicons-file-code-16: mkdocs.yml"

        ```yaml hl_lines="3-4"
        plugins:
          - pub-meta:
	          slug:
	            enable: true
        ```

> [!SETTINGS]+ [warn_on_missing](#+meta.slug.warn_on_missing){ #+meta.slug.warn_on_missing } (default: `true`)
> MkDocs contains a switch for [strict mode](https://www.mkdocs.org/user-guide/configuration/#strict). This mode forces break of document generation on any warning and if this option is also enabled, and it will force check all documents, contain a `slug` key defined.

    ===+ ":octicons-file-code-16: mkdocs.yml"

        ```yaml hl_lines="3-4"
        plugins:
          - pub-meta:
	          slug:
	            warn_on_missing: true
        ```

> [!SETTINGS]+ [key_name](#+meta.slug.key_name){ #+meta.slug.key_name } (default: `slug`)
>

#### Status

> [!SETTINGS]+ [search_in_hidden](#+meta.status.search_in_hidden){ #+meta.status.search_in_hidden } (default: `false`)
> When [Material for MkDocs search](https://squidfunk.github.io/mkdocs-material/setup/setting-up-site-search/#version-strings) plugin is enabled, by default, all documents are indexed and searchable (even those that are hidden by this plugin). To exclude hidden files from being searchable, normally you would have to [place an additional value](https://squidfunk.github.io/mkdocs-material/setup/setting-up-site-search/#search-exclusion) in each hidden document. To make things easier for you, the meta plugin handles it for you, and all hidden documents, are excluded from search. You can change this behavior by changing this value.

	===+ ":octicons-file-code-16: mkdocs.yml"

        ```yaml hl_lines="3-4"
        plugins:
          - pub-meta:
	          status:
	            search_in_hidden: false
        ```

> [!SETTINGS]+ [search_in_draft](#+meta.status.search_in_draft){ #+meta.status.search_in_draft } (default: `false`)
> When [Material for MkDocs search](https://squidfunk.github.io/mkdocs-material/setup/setting-up-site-search/#version-strings) plugin is enabled, by default, all documents are indexed and searchable (even those that are draft by this plugin). To exclude draft files from being searchable, normally you would have to [place an additional value](https://squidfunk.github.io/mkdocs-material/setup/setting-up-site-search/#search-exclusion) in each draft document. To make things easier for you, the meta plugin handles it for you, and all draft documents, are excluded from search. You can change this behavior by changing this value.

	===+ ":octicons-file-code-16: mkdocs.yml"

        ```yaml hl_lines="3-4"
        plugins:
          - pub-meta:
	          status:
	            search_in_draft: false
        ```

> [!SETTINGS]+ [file_default](#+meta.status.file_default){ #+meta.status.file_default } (default: `draft`)
> Defines default status of publication for documents. More information about this, you can find on this page in the section [document publication status](#Document%20publication%20status)

	===+ ":octicons-file-code-16: mkdocs.yml"

        ```yaml hl_lines="3-4"
        plugins:
          - pub-meta:
	          status:
	            file_default: draft
        ```

> [!SETTINGS]+ [file_warn_on_missing](#+meta.status.file_warn_on_missing){ #+meta.status.file_warn_on_missing } (default: `true`)
> MkDocs contains a switch for [strict mode](https://www.mkdocs.org/user-guide/configuration/#strict). This mode forces break of document generation on any warning and if this option is also enabled, and it will force check all documents, contain a `status` key defined.

    ===+ ":octicons-file-code-16: mkdocs.yml"

        ```yaml hl_lines="3-4"
        plugins:
          - pub-meta:
	          status:
	            file_arn_on_missing: true
        ```

> [!SETTINGS]+ [dir_default](#+meta.status.dir_default){ #+meta.status.dir_default } (default: `published`)
> Defines default status of publication for directories. More information about this, you can find on this page in the section [directory publication status](#Directory%20publication%20status).

	===+ ":octicons-file-code-16: mkdocs.yml"

        ```yaml hl_lines="3-4"
        plugins:
          - pub-meta:
	          status:
	            dir_default: published
        ```

> [!SETTINGS]+ [dir_warn_on_missing](#+meta.status.dir_warn_on_missing){ #+meta.status.dir_warn_on_missing } (default: `false`)
> MkDocs contains a switch for [strict mode](https://www.mkdocs.org/user-guide/configuration/#strict). This mode forces break of document generation on any warning and if this option is also enabled, and it will force check all directories (in fact `README.md` file in directory), contain a `status` key defined.

    ===+ ":octicons-file-code-16: mkdocs.yml"

        ```yaml hl_lines="3-4"
        plugins:
          - pub-meta:
	          status:
	            dir_warn_on_missing: false
        ```

> [!SETTINGS]+ [key_name](#+meta.status.key_name){ #+meta.status.key_name } (default: `status`)
> Metadata key name for status value.

    ===+ ":octicons-file-code-16: mkdocs.yml"

        ```yaml hl_lines="3-4"
        plugins:
          - pub-meta:
	          status:
	            key_name: status
        ```

#### Title

> [!SETTINGS]+ [key_name](#+meta.title.key_name){ #+meta.title.key_name } (default: `title`)
> Metadata key name for title value.

    ===+ ":octicons-file-code-16: mkdocs.yml"

        ```yaml hl_lines="3-4"
        plugins:
          - pub-meta:
	          title:
	            key_name: title
        ```
