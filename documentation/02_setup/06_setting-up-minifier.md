---
title: Setting up minifier
slug: pub-minifier
status: published
date: 2023-02-02 22:00:00
update: 2023-05-16 10:18:25
description: Setting up minifier plugin
categories: setup plugin minifier
---

# Setting up a minifier plugin

Even today, when most of us have quite fast internet connection, page size still matters to over feeling of fast page load and as one of the factors of SEO. For that reason, a good publishing tool, should allow optimizing image size and (less important) page code size optimization. Publisher for MkDocs has that ability, but it does not introduce new optimization algorithms, etc. It's using tools that are created by others and considered stable with a good performance, etc.

## Basic setup

To simplify the entire process, below is presented a single way of installation of all the tools. If you just want to use a single tool or learn more about what tool is used for what type of file, please take a look below for an [advanced setup](#advanced-setup) section where it's described.

### Tools installation

===+ ":simple-apple: MacOS"

    In MacOS, the easiest way to install any software, is to use a [Homebrew](https://brew.sh). You have to install it before. All the instructions can be found on project web page. After that the following commands have to be executed:

    ```commandline
    brew install pngquant oxipng mozjpeg node
    npm install -f --no-fund svgo html-minifier postcss cssnano postcss-svgo postcss-cli uglify-js
    ```

=== ":simple-windows: Windows"

    In Windows, the easiest way to install any software, is to use [Scoop](https://scoop.sh/). You have to install it before. All the instructions can be found on project web page. After that the following commands have to be executed:

    ```commandline
    scoop bucket add main
    scoop install pngquant oxipng nodejs mozjpeg
    npm install -f --no-fund svgo html-minifier postcss cssnano postcss-svgo postcss-cli uglify-js
    ```

=== ":simple-ubuntu: Ubuntu"

    In Ubuntu, the easiest way to install any software, is to use a built-in packages manager called `apt`, so you just have to execute the following commands:

    ```commandline
    sudo apt update
    sudo apt install rustc pngquant libjpeg-turbo-progs nodejs
    cargo install oxipng
    npm install --no-fund -f svgo html-minifier postcss cssnano postcss-svgo postcss-cli uglify-js
    ```

### Configuration

To enable the built-in optimization plugin, the following lines have to be added to `mkdocs.yml` file:

===+ ":octicons-file-code-16: mkdocs.yml"

    ```yaml hl_lines="2"
    plugins:
      - pub-minifier
    ```

Just like that, all optimization tools are enabled with optimal settings (according to my small experiments).

## Advanced setup

In day to day usage, those advanced settings, should probably not be touched. Those options are exposed, so you can adjust some settings offered by a given tool.

### Concurrency

File optimization process is a CPU intensive. Most modern computers have processors with multiple CPU cores. Each core can be used to optimize a single file. When your machine has more than one CPU core, it's good to have an ability to utilize all of them during the optimization process because it will reduce overall time needed for optimization of all files.

> [!SETTINGS]+ [threads](#+minifier.threads){ #+minifier.threads } (default: `0`)
> Defines how many CPUs the plugin will use for files optimization process. If set to 0 (default value) the plugin will read the number of available CPUs from system settings. To change the value of this setting, you have to edit a `mkdocs.yml` file:

    ===+ ":octicons-file-code-16: mkdocs.yml"

        ```yaml hl_lines="3"
        plugins:
          - pub-minifier:
              threads: 0
        ```

### Cache

When `pub-minifier` plugin is enabled, caching is enabled by default and cannot be turned off. Caching is quite crucial since image optimization is quite a time-consuming process (especially for PNG files).

The following configuration options are available for cache:

> [!SETTINGS]+ [cache_dir](#+minifier.cache_dir){ #+minifier.cache_dir } (default: `.cache`)
> Defines the directory location, where the cached files are stored.

    ===+ ":octicons-file-code-16: mkdocs.yml"

        To change the value of this setting, you have to edit a `mkdocs.yml` file:

        ```yaml hl_lines="3"
        plugins:
          - pub-minifier:
              cache_dir: .cache
        ```

    === ":fontawesome-solid-folder-tree:"

        By default, this directory is created on the same level as `docs` directory and the directory structure looks like this:

        ```commandline hl_lines="2"
            .
            ├─ .cache/
            ├─ docs/
            └─ mkdocs.yml
        ```

> [!SETTINGS]+ [cache_file](#+minifier.cache_file){ #+minifier.cache_file } (default: `.cache_file_list.yml`)
> Defines the name of the file, where all the data needed for proper cache working is stored. When this file is missing or corrupt, it and all cached files will be recreated. This file is stored inside the cache directory, and by default, the directory structure looks like this:

    ===+ ":octicons-file-code-16: mkdocs.yml"

        ```yaml hl_lines="3"
        plugins:
          - pub-minifier:
              cache_file: .cache_files_list.yml
        ```

    === ":fontawesome-solid-folder-tree:"

        ```commandline hl_lines="3"
            .
            ├─ .cache/
            │  └─ .cache_files_list.yml
            ├─ docs/
            └─ mkdocs.yml
        ```

### JPEG optimization

JPEG image file size optimizations are done using [MozJPEG](https://github.com/mozilla/mozjpeg) tool. As we can read on the project website:

> MozJPEG improves JPEG compression efficiency, achieving higher visual quality and smaller file sizes at the same time. It is compatible with the JPEG standard, and the vast majority of the world's deployed JPEG decoders.

Using this tool reduces JPEG image file size up to 30% with almost no visible quality degradation. You can always try to change it by modification of default settings. Please have in mind that default values were set after my personal experiments and not always can be the most optimal one.

#### Installation { #jpeg-optimization-installation }

If you already performed a [basic setup](#basic-setup) you already have this tool installed. If for any reasons you have to perform this operation separately, below you can find a set of commands that have to be executed to perform an installation.

===+ ":simple-apple: MacOS"

    In MacOS, the easiest way to install any software, is to use a [Homebrew](https://brew.sh). You have to install it before. All the instructions can be found on project web page. After that the following commands have to be executed:

    ```commandline
    brew install mozjpeg
    ```

=== ":simple-windows: Windows"

    In Windows, the easiest way to install any software, is to use [Scoop](https://scoop.sh/). You have to install it before. All the instructions can be found on project web page. After that the following commands have to be executed:

    ```commandline
    scoop bucket add main
    scoop install mozjpeg
    ```

=== ":simple-ubuntu: Ubuntu"

    In Ubuntu, the easiest way to install any software, is to use a built-in packages manager called `apt`, so you just have to execute the following commands:

    ```commandline
    sudo apt update
    sudo apt install libjpeg-turbo-progs
    ```

#### Settings { #jpeg-optimization-settings }

This section is on a #todo list.

### PNG optimization

PNG image file size optimizations are done using a combination of 2 tools:

1. [pngquant](https://pngquant.org) - this is a tool that reduces PNG file size by changing a color palette and alpha channel. Despite those optimizations, generated images are compatible with all web browsers and operating systems.
2. [oxipng](https://github.com/shssoichiro/oxipng) - this is a tool that reduces PNG file size by a lossless optimized compression algorithm.

Using those tools reduces PNG image file size by up to 70% with almost no visible quality degradation. You can always try to change it by modification of default settings. Please have in mind that default values were set after my personal experiments and not always can be the most optimal one.

<!--- #todo change above note to obsidian callout -->

#### Installation { #png-optimization-installation }

If you already performed a [basic setup](#basic-setup) you already have this tool installed. If for any reasons you have to perform this operation separately, below you can find a set of commands that have to be executed to perform an installation.

===+ ":simple-apple: MacOS"

    In MacOS, the easiest way to install any software, is to use a [Homebrew](https://brew.sh). You have to install it before. All the instructions can be found on project web page. After that the following commands have to be executed:

    ```commandline
    brew install pngquant oxipng
    ```

=== ":simple-windows: Windows"

    In Windows, the easiest way to install any software, is to use [Scoop](https://scoop.sh/). You have to install it before. All the instructions can be found on project web page. After that the following commands have to be executed:

    ```commandline
    scoop bucket add main
    scoop install pngquant oxipng
    ```

=== ":simple-ubuntu: Ubuntu"

    In Ubuntu, the easiest way to install any software, is to use a built-in packages manager called `apt`, so you just have to execute the following commands:

    ```commandline
    sudo apt update
    sudo apt install rustc pngquant
    cargo install oxipng
    ```

#### Settings { #png-optimization-settings }

This section is on a #todo list.

### SVG optimization

SVG vector image file size optimizations are done using [SVGO](https://github.com/svg/svgo) tool. This is a [Node.js-based](https://nodejs.org/) tool. As we can read on the project website:

> SVG files, especially those exported from various editors, usually contain a lot of redundant and useless information. This can include editor metadata, comments, hidden elements, default or non-optimal values and other stuff that can be safely removed or converted without affecting the SVG rendering result.

Using this tool reduces SVG vector image file size by up to 70% with no visible quality degradation. This tool has multiple plugins that impact the effectiveness of an optimization. At this time, the `pub-minifier` plugin doesn't allow changing the [default settings of used SVGO plugins](https://github.com/svg/svgo#built-in-plugins).

#### Installation { #svg-optimization-installation }

If you already performed a [basic setup](#basic-setup) you already have this tool installed. If for any reasons you have to perform this operation separately, below you can find a set of commands that have to be executed to perform an installation.

===+ ":simple-apple: MacOS"

    In MacOS, the easiest way to install any software, is to use a [Homebrew](https://brew.sh). You have to install it before. All the instructions can be found on project web page. After that the following commands have to be executed:

    ```commandline
    brew install node
    npm install -f --no-fund svgo
    ```

=== ":simple-windows: Windows"

    In Windows, the easiest way to install any software, is to use [Scoop](https://scoop.sh/). You have to install it before. All the instructions can be found on project web page. After that the following commands have to be executed:

    ```commandline
    scoop bucket add main
    scoop install nodejs
    npm install -f --no-fund svgo
    ```

=== ":simple-ubuntu: Ubuntu"

    In Ubuntu, the easiest way to install any software, is to use a built-in packages manager called `apt`, so you just have to execute the following commands:

    ```commandline
    sudo apt update
    sudo apt install nodejs
    npm install -f --no-fund svgo
    ```

#### Settings { #svg-optimization-settings }

This section is on a #todo list.

### HTML optimization

HTML file size optimizations are done using [html-minifier](https://github.com/kangax/html-minifier) tool. This is a [Node.js-based](https://nodejs.org/) tool. As we can read on the project website:

> HTMLMinifier is a highly **configurable**, **well-tested**, JavaScript-based HTML minifier.

Using this tool reduces HTML file size by up to 30%. You can always try to change it by modification of default settings. Please have in mind that default values were set after my personal experiments and not always can be the most optimal one.

#### Installation { #html-optimization-installation }

If you already performed a [basic setup](#basic-setup) you already have this tool installed. If for any reasons you have to perform this operation separately, below you can find a set of commands that have to be executed to perform an installation.

===+ ":simple-apple: MacOS"

    In MacOS, the easiest way to install any software, is to use a [Homebrew](https://brew.sh). You have to install it before. All the instructions can be found on project web page. After that the following commands have to be executed:

    ```commandline
    brew install node
    npm install -f --no-fund html-minifier
    ```

=== ":simple-windows: Windows"

    In Windows, the easiest way to install any software, is to use [Scoop](https://scoop.sh/). You have to install it before. All the instructions can be found on project web page. After that the following commands have to be executed:

    ```commandline
    scoop bucket add main
    scoop install nodejs
    npm install -f --no-fund html-minifier
    ```

=== ":simple-ubuntu: Ubuntu"

    In Ubuntu, the easiest way to install any software, is to use a built-in packages manager called `apt`, so you just have to execute the following commands:

    ```commandline
    sudo apt update
    sudo apt install nodejs
    npm install -f --no-fund html-minifier
    ```

#### Settings { #html-optimization-settings }

This section is on a #todo list.

### CSS optimization

CSS file size optimizations are done using [PostCSS](https://postcss.org) tool and some plugins:

- [PostCSS CLI](https://github.com/postcss/postcss-cli) - this is a Command Line Interface for this tool,
- [cssnano](https://github.com/cssnano/cssnano) - compression tool plugin,
- postcss-svgo - inline SVG files optimization plugin using an [SVGO](https://github.com/svg/svgo) tool (the same we are using for an [SVG file optimization](06_setting-up-minifier.md#svg-optimization)).

This is a [Node.js](https://nodejs.org/) based tool. As we can read on the project website:

> CSSNANO takes your nicely formatted CSS and runs it through many focused optimisations, to ensure that the final result is as small as possible for a production environment.

Using this tool reduces CSS file size by up to 30%. At this time, the `pub-minifier` plugin doesn't allow changing the [default settings of cssnano plugins](https://cssnano.co/docs/what-are-optimisations/#what-optimisations-do-you-support%3F).

#### Installation { #css-optimization-installation }

If you already performed a [basic setup](#basic-setup) you already have this tool installed. If for any reasons you have to perform this operation separately, below you can find a set of commands that have to be executed to perform an installation.

===+ ":simple-apple: MacOS"

    In MacOS, the easiest way to install any software, is to use a [Homebrew](https://brew.sh). You have to install it before. All the instructions can be found on project web page. After that the following commands have to be executed:

    ```commandline
    brew install node
    npm install -f --no-fund postcss cssnano postcss-svgo postcss-cli
    ```

=== ":simple-windows: Windows"

    In Windows, the easiest way to install any software, is to use [Scoop](https://scoop.sh/). You have to install it before. All the instructions can be found on project web page. After that the following commands have to be executed:

    ```commandline
    scoop bucket add main
    scoop install nodejs
    npm install -f --no-fund postcss cssnano postcss-svgo postcss-cli
    ```

=== ":simple-ubuntu: Ubuntu"

    In Ubuntu, the easiest way to install any software, is to use a built-in packages manager called `apt`, so you just have to execute the following commands:

    ```commandline
    sudo apt update
    sudo apt install nodejs
    npm install -f --no-fund postcss cssnano postcss-svgo postcss-cli
    ```

#### Settings { #css-optimization-settings }

This section is on a #todo list.

### JS optimization

JS file size optimizations are done using [UglifyJS](https://github.com/mishoo/UglifyJS) tool. This is a [Node.js-based](https://nodejs.org/) tool. As we can read on the project website:

> UglifyJS is a JavaScript parser, minifier, compressor and beautifier toolkit.

Using this tool reduces JS file size by up to 20%. At this time, the `pub-minifier` plugin doesn't allow changing the default settings.

#### Installation { #js-optimization-installation }

If you already performed a [basic setup](#basic-setup) you already have this tool installed. If for any reasons you have to perform this operation separately, below you can find a set of commands that have to be executed to perform an installation.

===+ ":simple-apple: MacOS"

    In MacOS, the easiest way to install any software, is to use a [Homebrew](https://brew.sh). You have to install it before. All the instructions can be found on project web page. After that the following commands have to be executed:

    ```commandline
    brew install node
    npm install -f --no-fund uglify-js
    ```

=== ":simple-windows: Windows"

    In Windows, the easiest way to install any software, is to use [Scoop](https://scoop.sh/). You have to install it before. All the instructions can be found on project web page. After that the following commands have to be executed:

    ```commandline
    scoop bucket add main
    scoop install nodejs
    npm install -f --no-fund uglify-js
    ```

=== ":simple-ubuntu: Ubuntu"

    In Ubuntu, the easiest way to install any software, is to use a built-in packages manager called `apt`, so you just have to execute the following commands:

    ```commandline
    sudo apt update
    sudo apt install nodejs
    npm install -f --no-fund uglify-js
    ```

#### Settings { #js-optimization-settings }

This section is on a #todo list.
