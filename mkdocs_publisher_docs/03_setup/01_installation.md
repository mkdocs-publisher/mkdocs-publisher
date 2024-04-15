---
title: Installation
icon: material/laptop
slug: installation
publish: true
date: 2023-03-16 18:27:00
update: 2023-10-10 13:55:56
description: Installation
categories:
  - start
---


# Installation

All plugins are part of this package and cannot be installed separately, but not all of them have to be enabled.

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
- [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) - (probably) the best theme for MkDocs,
- [PyMdown Extensions](https://python-markdown.github.io/extensions/) - extensions for Markdown language.

There are also some external tools used, mostly by `pub-minifier` plugin. Since this plugin is part of this package, but it's optional to use (not enabled by default), the process of installation of those tools is described in this [plugin installation](03_seo_and_sharing/02_setting-up-minifier.md#tools-installation).
