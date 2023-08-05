---
title: Development
slug: development
status: published
date: 2023-03-21 11:27:00
update: 2023-08-01 12:00:42
description: Development of this plugin how to
categories:
  - general
  - development
---

# Development

## Install as editable library


===+ "pip"

    ```bash
    pip install --editable ../mkdocs-publisher/
    ```

=== "poetry"

    ```bash
    poetry add --editable ../mkdocs-publisher/
    ```

## Install from build package

===+ "pip"

    ```bash
    pip install ../mkdocs-publisher/dist/mkdocs-publisher-0.4.1.tar.gz
    ```

=== "poetry"

    ```bash
    poetry add ../mkdocs-publisher/dist/mkdocs-publisher-0.4.1.tar.gz
    ```

## Remove from dependencies

===+ "pip"

    ```bash
    pip uninstall mkdocs-publisher
    ```

=== "poetry"

    ```bash
    poetry remove mkdocs-publisher
    ```
