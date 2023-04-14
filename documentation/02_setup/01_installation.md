---
title: Installation
slug: installation
status: published
date: 2023-03-16 18:27:00
categories: start
description: Installation
---

# Installation

All plugins are part of this package and cannot be installed separately, but not all of them have to be enabled (more about this you can find in the [Setup section](01_installation.md)).

Publisher for MkDocs is a Python package that can be installed using `pip` (ideally inside a virtual environment) or any other package manager like `poetry` that handles virtual management out of the box.

===+ "pip"

    ```bash
    pip install mkdocs-publisher
    ```

=== "poetry"

    ```bash
    poetry add mkdocs-publisher
    ```

This package depends on some other Python packages and MkDocs plugins, so during installation they will also be installed. List of them:

- [MkDocs](https://www.mkdocs.org),
- [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) - probably the best theme for MkDocs,
- [PyMdown Extensions](https://python-markdown.github.io/extensions/) - extensions for Markdown language.

There are also some external tools used, mostly by `pub-minifier` plugin. Since this plugin is part of this package, but it's optional to use (not enabled by default), the process of installation of those tools is described in this plugin installation.
