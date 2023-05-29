---
title: Setting up meta
slug: pub-meta
status: published
date: 2023-05-15 16:00:00
update: 2023-05-22 13:33:20
description: Setting up the meta plugin for metadata retrival and automatic navigation building
categories: setup plugin meta
---

# Setting up the meta plugin

## Introduction

As you can see on the left - side menu, this plugin is placed as the first one because this plugin can be considered as one that influences the way, you will be writing a documentation. So, why it's so essential? There are a few reasons:

1. Automatic navigation building based on file and directory names. This simplifies a process of a document navigation creation in `mkdocs.yml` file, described in [official documentation](https://www.mkdocs.org/user-guide/writing-your-docs/#configure-pages-and-navigation).
2. Based on file meta-data, you can set document:
	- URL,
	- creation/update date,
	- document publication state,
	- and some other less important.
	Most of these options, influence the SEO of the page build using MkDocs.

Probably you are now wondering why 2 quite different functionalities are placed in one plugin?

The answer is not so obvious and a bit technical, but in bigger simplification, it's way simpler and less complex to bound those functionalities together. The main reason for that is how MkDocs internals work. For example, when navigation is built and when final HTML files are generated. Other example could be a document status implementation that influences navigation building, file list creation and `sitemap.xml` creation. This process should be considered as one functionality and splitting it over 2 separate plugins is possible, but it will not only increase code complexity, but also will increase significantly complexity of configuration since many settings used for automatic navigation building are the same for defining file meta-data. So, if we split functionality into 2 separate plugins, the final user (You) will have to maintain consistency in `mkdocs.yml` file. With a single plugin approach, we can reduce this problem to just maintaining a single point of configuration and settings validation.

> [!warning] Important information
> However, this plugin is not needed for other plugins to work correctly, it's highly recommended to use it.

## Document meta-data

Markdown documents can contain additional metadata that is not rendered by MkDocs. This metadata is located at the beginning of the file (more information about this you can found in MkDocs documentation in [Meta-Data section](https://www.mkdocs.org/user-guide/writing-your-docs/#meta-data)).

MkDocs supports 2 main formats of meta-data:

===+ "YAML Style Meta-Data (preferred)"

	It's preferred style since more plugins supports it and its the same format as in `mkdocs.yml` file. Also this format is supported by other tools (like [Jekyll](https://jekyllrb.com/docs/front-matter/) that is used in GitHub or [GitLab](https://docs.gitlab.com/ee/user/markdown.html#front-matter))

	```markdown
	---
	title: Your document title
	description: A short description of document content that encourage to read it
	---

	This is the first paragraph of the document.
	```

=== "MultiMarkdown Style Meta-Data"

	This style is NOT prefered since not all plugins and other tools supports it.

	```markdown
	Title: Your document title
	Description: A short description of document content that encourage to read it

	This is the first paragraph of the document.
	```

> [!info] YAML front matter
> Since the YAML front matter format for meta-data is used by a wider set of other plugins and tools, this format will be used in this tool documentation.

## Navigation automatic generation



## Configuration

### Enable meta plugin

To enable the built-in meta plugin, the following lines have to be added to `mkdocs.yml` file:

===+ ":octicons-file-code-16: mkdocs.yml"

    ```yaml hl_lines="2"
    plugins:
      - pub-meta
    ```

### Settings
