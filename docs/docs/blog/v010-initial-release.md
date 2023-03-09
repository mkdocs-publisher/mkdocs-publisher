---
title: v0.1.0 - Initial release
slug: v010-initial-release
status: published
date: 2023-02-02 22:00:00
tags: v0.1.0
categories: release
description: Initial version of MkDosc Blog-in plugin
---

### Another blogging plugin for MkDocs? But why?

The simplest answer is: because I couldn't find one good enough (and free).

The flip side of the same coin was that I wanted to migrate my personal blog related to [testing](https://testerembyc.pl) (sorry only in Polish, but you can try to use Google translator) from [Nikola](https://getnikola.com/) that works quite well, but sometimes is overly complicated, has almost none search functionality and markdown files are not the default one (but it's possible to use them). Why does the Markdown format is so important? Because I love [Obsidian](https://obsidian.md) as a tool for gathering knowledge, and this format is a crucial part of that tool.

At the time when this plugin was created, there were no free and good alternatives. The only one that could be good enough was hidden behind a paid wall and was a part of a theme [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/blog/). Some of the ideas for this plugin and functionalities came from documentation of the Material for MkDocs theme, Nikola and other plugins.

Existing alternatives (with my comment):

- [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/blog/) - complex solution, but paid,
- [mkdocs-blogging-plugin](https://github.com/liang2kl/mkdocs-blogging-plugin) - works, but simple solution for simple blog (limited tags usage, theme files modification needed, limited use of frontmatter, limited number of features),
- [mkdocs-blog-plugin](https://github.com/fmaida/mkdocs-blog-plugin) - no longer maintained and simple,
- [python-mkblog](https://github.com/derJD/python-mkblog) - no longer maintained and simple,
- [mkdocs-blog](https://github.com/andyoakley/mkdocs-blog) - no longer maintained and simple,
- [material theme modification](https://www.dirigible.io/blogs/2021/11/2/material-blogging-capabilities/) - it's not a plugin, but a complete theme modification, it's hard to extend and configure.

As you can see, there are just 2 still maintained plugins for blogging in MkDocs:

1. Material for MkDocs - complex but paid,
2. mkdosc-blogging-plugin - much simpler than Material for MkDocs.

### Features implemented

This project is now at an early stage of development. Current functionalities are:

- blog post update date based on metadata (post YAML frontmatter)
- blog post URL link based on metadata (post YAML frontmatter)
- blog post tags and categories based on metadata (post YAML frontmatter)
- support for blog post teaser
- auto generation of blog posts navigation
