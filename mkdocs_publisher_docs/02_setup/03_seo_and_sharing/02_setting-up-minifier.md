---
title: Setting up minifier
icon: material/run-fast
slug: pub-minifier
publish: true
date: 2023-02-02 22:00:00
update: 2023-10-17 16:15:52
description: Setting up Publisher for MkDocs minifier plugin for page size optimization
categories:
  - setup
  - plugin
  - minifier
---

# Setting up a minifier plugin

## Introduction

Even today, when most of us have quite fast internet connection, page size still matters to over feeling of fast page load and as one of the factors of SEO. For that reason, a good publishing tool, should allow optimizing image size and (less important) page code size optimization. Publisher for MkDocs has that ability, but it does not introduce new optimization algorithms, etc. It's using tools that are created by others and considered stable with a good performance, etc.

## Installation

To simplify the entire process, below is presented a single way of installation of all the tools. If you just want to use a single tool or learn more about what tool is used for what type of file, please take a look below for a [configuration](#configuration) section where it's described.

===+ ":simple-apple: MacOS"

    In macOS, the easiest way to install any software, is to use a [Homebrew](https://brew.sh). You have to install it before. All the instructions can be found on project web page.

	===+ ":material-file: All"

	    ```console
	    brew install pngquant oxipng mozjpeg node
	    npm install -f --no-fund svgo html-minifier postcss cssnano postcss-svgo postcss-cli uglify-js
	    ```

	=== ":material-file-png-box: PNG"

		```console
	    brew install pngquant oxipng
	    ```

	=== ":material-file-jpg-box: JPEG"

		```console
	    brew install mozjpeg
	    ```

	=== ":simple-svgo: SVG"

		```console
	    brew install node
	    npm install -f --no-fund svgo
	    ```

	=== ":simple-html5: HTML"

		```console
	    brew install node
	    npm install -f --no-fund html-minifier
	    ```

	=== ":simple-css3: CSS"

		```console
	    brew install node
	    npm install -f --no-fund postcss cssnano postcss-svgo postcss-cli
	    ```

	=== ":simple-javascript: JS"

		```console
	    brew install node
	    npm install -f --no-fund uglify-js
	    ```

=== ":simple-windows: Windows"

    In Windows, the easiest way to install any software, is to use [Scoop](https://scoop.sh/). You have to install it before. All the instructions can be found on project web page.

	===+ ":material-file: All"

	    ```console
	    scoop bucket add main
		scoop install pngquant oxipng mozjpeg nodejs
		npm install -f --no-fund svgo html-minifier postcss cssnano postcss-svgo postcss-cli uglify-js
	    ```

	=== ":material-file-png-box: PNG"

		```console
	    scoop install pngquant oxipng
	    ```

	=== ":material-file-jpg-box: JPEG"

		```console
	    scoop install mozjpeg
	    ```

	=== ":simple-svgo: SVG"

		```console
	    scoop install nodejs
	    npm install -f --no-fund svgo
	    ```

	=== ":simple-html5: HTML"

		```console
	    scoop install nodejs
	    npm install -f --no-fund html-minifier
	    ```

	=== ":simple-css3: CSS"

		```console
	    scoop install nodejs
	    npm install -f --no-fund postcss cssnano postcss-svgo postcss-cli
	    ```

	=== ":simple-javascript: JS"

		```console
	    scoop install nodejs
	    npm install -f --no-fund uglify-js
	    ```


=== ":simple-ubuntu: Ubuntu"

    In Ubuntu, the easiest way to install any software, is to use a built-in packages manager called `apt`.

	===+ ":material-file: All"

	    ```console
		sudo apt update
		sudo apt install -y rustc pngquant libjpeg-turbo-progs nodejs
		cargo install oxipng
		npm install --no-fund -f svgo html-minifier postcss cssnano postcss-svgo postcss-cli uglify-js
	    ```

	=== ":material-file-png-box: PNG"

		```console
	    sudo apt update
		sudo apt install -y rustc pngquant
		cargo install oxipng
	    ```

	=== ":material-file-jpg-box: JPEG"

		```console
	    sudo apt update
		sudo apt install -y libjpeg-turbo-progs
	    ```

	=== ":simple-svgo: SVG"

		```console
	    sudo apt update
		sudo apt install nodejs
		npm install --no-fund -f svgo
	    ```

	=== ":simple-html5: HTML"

		```console
	    sudo apt update
		sudo apt install nodejs
		npm install --no-fund -f html-minifier
	    ```

	=== ":simple-css3: CSS"

		```console
	    sudo apt update
		sudo apt install nodejs
		npm install --no-fund -f postcss cssnano postcss-svgo postcss-cli
	    ```

	=== ":simple-javascript: JS"

		```console
	    sudo apt update
		sudo apt install nodejs
		npm install --no-fund -f uglify-js
	    ```

## Configuration

To enable the built-in optimization plugin, the following lines have to be added to `mkdocs.yml` file:

===+ ":octicons-file-code-16: mkdocs.yml"

    ```yaml hl_lines="2"
    plugins:
      - pub-minifier
    ```

Just like that, all optimization tools are enabled with optimal settings (according to my small experiments).

### General

> [!WARNING] Advanced settings
> In day to day usage, those settings should be considered as advanced and probably shouldn't be changed. Those options are exposed, so you can adjust some settings offered by a given tool, but you should test those options locally.


===+ ":octicons-file-code-16: mkdocs.yml"

	```yaml hl_lines="3-7"
	plugins:
	  - pub-minifier:
	      cache_enabled: true
		  cache_dir: .pub_min_cache
		  cache_file: .cache_files_list.yml
		  exclude: []
		  threads: 0
	```

=== ":fontawesome-solid-folder-tree:"

	By default, this directory is created on the same level as `docs` directory and the directory structure looks like this:

	```commandline hl_lines="2-3"
		.
		├─ .pub_min_cache/
		│  └─ .cache_files_list.yml
		├─ docs/
		└─ mkdocs.yml
	```

> [!SETTINGS]- [cache_enabled](#+minifier.cache_enabled){#+minifier.cache_enabled}
> Control if caching mechanism is enabled. When it's enabled, you can still disable cache per each file type.

> [!SETTINGS]- [cache_dir](#+minifier.cache_dir){#+minifier.cache_dir}
> Defines the directory location, where the cached files are stored.

> [!SETTINGS]- [cache_file](#+minifier.cache_file){#+minifier.cache_file}
> Defines the name of the file, where all the data needed for proper cache working is stored. When this file is missing or corrupt, it and all cached files will be recreated. This file is stored inside the cache directory, and by default, the directory structure looks like this:

> [!SETTINGS]- [exclude](#+minifier.exclude){#+minifier.exclude}
> Defines a list of exclusion patterns for files or directories that will not be minified. Each file type has its own exclusion list that inherits values from this one, so you don't have to add the same values.

> [!SETTINGS]- [threads](#+minifier.threads){#+minifier.threads}
> File optimization process is a CPU intensive. Most modern computers have processors with multiple CPU cores. Each core can be used to optimize a single file. When your machine has more than one CPU core, it's good to have an ability to utilize all of them during the optimization process because it will reduce overall time needed for optimization of all files. This setting defines how many CPUs the plugin will use for file optimization process. If set to 0 (default value) the plugin will read the number of available CPUs from system settings.

### JPEG optimization

JPEG image file size optimizations are done using [MozJPEG](https://github.com/mozilla/mozjpeg) tool. As we can read on the project website:

> [!QUOTE] MozJPEG
> MozJPEG improves JPEG compression efficiency, achieving higher visual quality and smaller file sizes at the same time. It is compatible with the JPEG standard, and the vast majority of the world's deployed JPEG decoders.

Using this tool reduces JPEG image file size up to 30% with almost no visible quality degradation. You can always try to change it by modification of default settings. Please have in mind that default values were set after my personal experiments and not always can be the most optimal one.

``` yaml hl_lines="3-16"
plugins:
  - pub-minifier:
	jpeg:
	    cache_enabled: true
		enabled: true
		enabled_on_serve: false
		exclude: []
		extensions: [".[jJ][pP][gG]", ".[jJ][pP][eE][gG]"]
		djpeg_path: djpeg
		cjpeg_path: cjpeg
		jpegtran_path: jpegtran
		optimise: true
		progressive: true
		copy_meta: none
		smooth: 10
		quality: 85
```

Above you can find all possible settings with their default values. You don't have to provide them. Just use them if you want to change some settings. The description of the meaning of given setting, you can find below.

> [!SETTINGS]- [cache_enabled](#+minifier.jpeg.cache_enabled){#+minifier.jpeg.cache_enabled}
> Control if caching mechanism is enabled.

> [!SETTINGS]- [enabled](#+minifier.jpeg.enabled){#+minifier.jpeg.enabled}
> Control if JPEG minifier is enabled.

> [!SETTINGS]- [enabled_on_serve](#+minifier.jpeg.enabled_on_serve){#+minifier.jpeg.enabled_on_serve}
> Control if JPEG minifier is enabled while page is being served locally (mostly used for content creation).

> [!SETTINGS]- [exclude](#+minifier.jpeg.exclude){#+minifier.jpeg.exclude}
> Defines a list of exclusion patterns for files or directories that will not be minified.

> [!SETTINGS]- [exclude](#+minifier.jpeg.extensions){#+minifier.jpeg.extensions}
> Defines a list of file extensions that will be minified.

> [!SETTINGS]- [djpeg_path](#+minifier.jpeg.djpeg_path){#+minifier.jpeg.djpeg_path}
> Path to `djpeg` tool (part of MozJPEG package).

> [!SETTINGS]- [cjpeg_path](#+minifier.jpeg.cjpeg_path){#+minifier.jpeg.cjpeg_path}
> Path to `cjpeg` tool (part of MozJPEG package).

> [!SETTINGS]- [jpegtran_path](#+minifier.jpeg.jpegtran_path){#+minifier.jpeg.jpegtran_path}
> Path to `jpegtran` tool (part of MozJPEG package).

> [!SETTINGS]- [optimise](#+minifier.jpeg.optimise){#+minifier.jpeg.optimise}
> Optimize Huffman table (smaller file, but slow compression).

> [!SETTINGS]- [progressive](#+minifier.jpeg.progressive){#+minifier.jpeg.progressive}
> Create progressive JPEG file.

> [!SETTINGS]- [copy_meta](#+minifier.jpeg.copy_meta){#+minifier.jpeg.copy_meta}
> Defines what metadata to copy: `none`, `comments`, `icc` or `all`.

> [!SETTINGS]- [smooth](#+minifier.jpeg.smooth){#+minifier.jpeg.smooth}
> Level of image smoothness: `0`(disabled, smallest) - `100`(biggest) [default: `10`].

> [!SETTINGS]- [quality](#+minifier.jpeg.quality){#+minifier.jpeg.quality}
> Level of compression: `0`(disabled, worst) - `100` (best) [default: `85`].

### PNG optimization

PNG image file size optimizations are done using a combination of 2 tools:

1. [pngquant](https://pngquant.org) - this is a tool that reduces PNG file size by changing a color palette and alpha channel. Despite those optimizations, generated images are compatible with all web browsers and operating systems.
2. [oxipng](https://github.com/shssoichiro/oxipng) - this is a tool that reduces PNG file size by a lossless optimized compression algorithm.

Using those tools together, can reduce PNG image file size by up to 70% with almost no visible quality degradation. You can always try to change it by modifying of default settings. Please have in mind that default values were set after my personal experiments and not always can be the most optimal one.

``` yaml hl_lines="3-16"
plugins:
  - pub-minifier:
	png:
		cache_enabled: true
		enabled: true
		enabled_on_serve: false
		exclude: []
		extensions: [".[pP][nN][gG]"]
		pngquant_enabled: true
		pngquant_path: ongquant
		pngquant_speed: 1
		pngquant_quality: 95
		oxipng_enabled: true
		oxipng_path: oxipng
		oxipng_max_compression: true
		strip: true
```

Above you can find all possible settings with their default values. You don't have to provide them. Just use them if you want to change some settings. The description of the meaning of given setting, you can find below.

> [!SETTINGS]- [cache_enabled](#+minifier.png.cache_enabled){#+minifier.png.cache_enabled}
> Control if caching mechanism is enabled.

> [!SETTINGS]- [enabled](#+minifier.png.enabled){#+minifier.png.enabled}
> Control if PNG minifier is enabled.

> [!SETTINGS]- [enabled_on_serve](#+minifier.png.enabled_on_serve){#+minifier.png.enabled_on_serve}
> Control if PNG minifier is enabled while page is being served locally (mostly used for content creation).

> [!SETTINGS]- [exclude](#+minifier.png.exclude){#+minifier.png.exclude}
> Defines a list of exclusion patterns for files or directories that will not be minified.

> [!SETTINGS]- [exclude](#+minifier.png.extensions){#+minifier.png.extensions}
> Defines a list of file extensions that will be minified.

> [!SETTINGS]- [pngquant_enabled](#+minifier.png.pngquant_enabled){#+minifier.png.pngquant_enabled}
> Control if **pngquant** tool is enabled.

> [!SETTINGS]- [pngquant_path](#+minifier.png.pngquant_path){#+minifier.png.pngquant_path}
> Path to `pnquant` tool.

> [!SETTINGS]- [pngquant_speed](#+minifier.png.pngquant_speed){#+minifier.png.pngquant_speed}
> Compression speed: `1` (slow but best quality) - `12` (fast but rough) [default: `1`].

> [!SETTINGS]- [pngquant_quality](#+minifier.png.pngquant_quality){#+minifier.png.pngquant_quality}
> Image quality: `0` (worst) - `100` (best) [default: `95`]

> [!SETTINGS]- [oxipng_enabled](#+minifier.png.oxipng_enabled){#+minifier.png.oxipng_enabled}
> Control if **oxipng** tool is enabled.

> [!SETTINGS]- [oxipng_path](#+minifier.png.oxipng_path){#+minifier.png.oxipng_path}
> Path to `oxipng`.

> [!SETTINGS]- [oxipng_max_compression](#+minifier.png.oxipng_path){#+minifier.png.oxipng_max_compression}
> Use max possible compression.

> [!SETTINGS]- [strip](#+minifier.png.oxipng_path){#+minifier.png.strip}
> Strip metadata from file.

### SVG optimization

SVG vector image file size optimizations are done using [SVGO](https://github.com/svg/svgo) tool. This is a [Node.js-based](https://nodejs.org/) tool. As we can read on the project website:

> [!QUOTE] SVGO
> SVG files, especially those exported from various editors, usually contain a lot of redundant and useless information. This can include editor metadata, comments, hidden elements, default or non-optimal values and other stuff that can be safely removed or converted without affecting the SVG rendering result.

Using this tool reduces SVG vector image file size by up to 70% with no visible quality degradation. This tool has multiple plugins that impact the effectiveness of an optimization. At this time, the `pub-minifier` plugin doesn't allow changing the [default settings of used SVGO plugins](https://github.com/svg/svgo#built-in-plugins).

``` yaml hl_lines="3-10"
plugins:
  - pub-minifier:
	svg:
		cache_enabled: true
		enabled: true
		enabled_on_serve: false
		exclude: []
		extensions: [".[sS][vV][gG]"]
		svgo_path: svgo
		multipass: true
```

Above you can find all possible settings with their default values. You don't have to provide them. Just use them if you want to change some settings. The description of the meaning of given setting, you can find below.

> [!SETTINGS]- [cache_enabled](#+minifier.svg.cache_enabled){#+minifier.svg.cache_enabled}
> Control if caching mechanism is enabled.

> [!SETTINGS]- [enabled](#+minifier.svg.enabled){#+minifier.svg.enabled}
> Control if SVG minifier is enabled.

> [!SETTINGS]- [enabled_on_serve](#+minifier.svg.enabled_on_serve){#+minifier.svg.enabled_on_serve}
> Control if SVG minifier is enabled while page is being served locally (mostly used for content creation).

> [!SETTINGS]- [exclude](#+minifier.svg.exclude){#+minifier.svg.exclude}
> Defines a list of exclusion patterns for files or directories that will not be minified.

> [!SETTINGS]- [exclude](#+minifier.svg.extensions){#+minifier.svg.extensions}
> Defines a list of file extensions that will be minified.

> [!SETTINGS]- [svgo_path](#+minifier.svg.svgo_path){#+minifier.svg.svgo_path}
> Path to `svgo` tool.

> [!SETTINGS]- [multipass](#+minifier.svg.multipass){#+minifier.svg.multipass}
> Do multiple passes during compression to ensure all optimizations are apllied.

### HTML optimization

HTML file size optimizations are done using [html-minifier](https://github.com/kangax/html-minifier) tool. This is a [Node.js-based](https://nodejs.org/) tool. As we can read on the project website:

> [!QUOTE] HTMLMinifier
> HTMLMinifier is a highly **configurable**, **well-tested**, JavaScript-based HTML minifier.

Using this tool reduces HTML file size by up to 30%. You can always try to change it by modification of default settings. Please have in mind that default values were set after my personal experiments and not always can be the most optimal one.

``` yaml hl_lines="3-21"
plugins:
  - pub-minifier:
	html:
		cache_enabled: true
		enabled: true
		enabled_on_serve: false
		exclude: []
		extensions: [".[hH][tT][mM]", ".[hH][tT][mM][lL]"]
		postcss_path: postcss
		case_sensitive: true
		minify_css: true
		minify_js: true
		remove_comments: true
		remove_tag_whitespace: false
		collapse_whitespace: true
		conservative_collapse: true
		collapse_boolean_attributes: true
		preserve_line_breaks: true
		sort_attributes: true
		sort_class_name: true
		max_line_length: 1024
```

Above you can find all possible settings with their default values. You don't have to provide them. Just use them if you want to change some settings. The description of the meaning of given setting, you can find below.

> [!SETTINGS]- [cache_enabled](#+minifier.html.cache_enabled){#+minifier.html.cache_enabled}
> Control if caching mechanism is enabled.

> [!SETTINGS]- [enabled](#+minifier.html.enabled){#+minifier.html.enabled}
> Control if HTML minifier is enabled.

> [!SETTINGS]- [enabled_on_serve](#+minifier.html.enabled_on_serve){#+minifier.html.enabled_on_serve}
> Control if HTML minifier is enabled while page is being served locally (mostly used for content creation).

> [!SETTINGS]- [exclude](#+minifier.html.exclude){#+minifier.html.exclude}
> Defines a list of exclusion patterns for files or directories that will not be minified.

> [!SETTINGS]- [exclude](#+minifier.html.extensions){#+minifier.html.extensions}
> Defines a list of file extensions that will be minified.

> [!SETTINGS]- [html_minifier_path](#+minifier.html.html_minifier_path){#+minifier.html.html_minifier_path}
> Path to `html-minifier` tool.

> [!SETTINGS]- [case_sensitive](#+minifier.html.case_sensitive){#+minifier.html.case_sensitive}
> Treat attributes in case sensitive manner.

> [!SETTINGS]- [minify_css](#+minifier.html.minify_css){#+minifier.html.minify_css}
> Minify CSS that is inside HTML (using `celan-css`)

> [!SETTINGS]- [minify_js](#+minifier.html.minify_js){#+minifier.html.minify_js}
> Minify JS that is inside HTML (using `uglify-js`).

> [!SETTINGS]- [remove_comments](#+minifier.html.remove_comments){#+minifier.html.remove_comments}
> Strip HTML comments.

> [!SETTINGS]- [remove_tag_whitespace](#+minifier.html.remove_tag_whitespace){#+minifier.html.remove_tag_whitespace}
> Remove space between attributes whenever possible.
>
> > [!DANGER]+ Danger !!!
> > Enabling this setting may lead to problems with code blocks, etc.

> [!SETTINGS]- [collapse_whitespace](#+minifier.html.collapse_whitespace){#+minifier.html.collapse_whitespace}
> Collapse white space that contributes to text nodes in a document tree.

> [!SETTINGS]- [conservative_collapse](#+minifier.html.conservative_collapse){#+minifier.html.conservative_collapse}
> Always collapse to 1 space (never remove it entirely).

> [!SETTINGS]- [collapse_boolean_attributes](#+minifier.html.collapse_boolean_attributes){#+minifier.html.collapse_boolean_attributes}
> Omit attribute values from boolean attributes.

> [!SETTINGS]- [preserve_line_breaks](#+minifier.html.preserve_line_breaks){#+minifier.html.preserve_line_breaks}
> Always collapse to 1 line break (never remove it entirely) when whitespace between tags include a line break.

> [!SETTINGS]- [sort_attributes](#+minifier.html.sort_attributes){#+minifier.html.sort_attributes}
> Sort attributes by frequency.

> [!SETTINGS]- [sort_class_name](#+minifier.html.sort_class_name){#+minifier.html.sort_class_name}
> Sort style classes by frequency.

> [!SETTINGS]- [max_line_length](#+minifier.html.max_line_length){#+minifier.html.max_line_length}
> Define max line length after optimization: `80` - `4096` [default: `1024`].

### CSS optimization

CSS file size optimizations are done using [PostCSS](https://postcss.org) tool and some plugins:

- [PostCSS CLI](https://github.com/postcss/postcss-cli) - this is a Command Line Interface for this tool,
- [cssnano](https://github.com/cssnano/cssnano) - compression tool plugin,
- postcss-svgo - inline SVG files optimization plugin using an [SVGO](https://github.com/svg/svgo) tool (the same we are using for an [SVG file optimization](02_setting-up-minifier.md#svg-optimization)).

This is a [Node.js](https://nodejs.org/) based tool. As we can read on the project website:

> [!QUOTE] CSSnano
> CSSnano takes your nicely formatted CSS and runs it through many focused optimisations, to ensure that the final result is as small as possible for a production environment.

Using this tool reduces CSS file size by up to 30%. At this time, the `pub-minifier` plugin doesn't allow changing the [default settings of cssnano](https://cssnano.co/docs/what-are-optimisations/#what-optimisations-do-you-support%3F).

``` yaml hl_lines="3-10"
plugins:
  - pub-minifier:
	css:
		cache_enabled: true
		enabled: true
		enabled_on_serve: false
		exclude: []
		extensions: [".[cC][sS][sS]"]
		postcss_path: postcss
		skip_minified: true
```

Above you can find all possible settings with their default values. You don't have to provide them. Just use them if you want to change some settings. The description of the meaning of given setting, you can find below.

> [!SETTINGS]- [cache_enabled](#+minifier.css.cache_enabled){#+minifier.css.cache_enabled}
> Control if caching mechanism is enabled.

> [!SETTINGS]- [enabled](#+minifier.css.enabled){#+minifier.css.enabled}
> Control if CSS minifier is enabled.

> [!SETTINGS]- [enabled_on_serve](#+minifier.css.enabled_on_serve){#+minifier.css.enabled_on_serve}
> Control if CSS minifier is enabled while page is being served locally (mostly used for content creation).

> [!SETTINGS]- [exclude](#+minifier.css.exclude){#+minifier.css.exclude}
> Defines a list of exclusion patterns for files or directories that will not be minified.

> [!SETTINGS]- [exclude](#+minifier.css.extensions){#+minifier.css.extensions}
> Defines a list of file extensions that will be minified.

> [!SETTINGS]- [postcss_path](#+minifier.css.postcss_path){#+minifier.css.postcss_path}
> Path to `postcss` tool.

> [!SETTINGS]- [skip_minified](#+minifier.css.skip_minified){#+minifier.css.skip_minified}
> Skip files that are already minified (usually one with `.min.css` extension).

### JS optimization

JS file size optimizations are done using [UglifyJS](https://github.com/mishoo/UglifyJS) tool. This is a [Node.js-based](https://nodejs.org/) tool. As we can read on the project website:


> [!QUOTE] UglifyJS
> UglifyJS is a JavaScript parser, minifier, compressor and beautifier toolkit.

Using this tool reduces JS file size by up to 20%. At this time, the `pub-minifier` plugin doesn't allow changing the default settings.

``` yaml hl_lines="3-10"
plugins:
  - pub-minifier:
	js:
		cache_enabled: true
		enabled: true
		enabled_on_serve: false
		exclude: []
		extensions: [".[jJ][sS]"]
		uglifyjs_path: uglifyjs
		skip_minified: true
```

Above you can find all possible settings with their default values. You don't have to provide them. Just use them if you want to change some settings. The description of the meaning of given setting, you can find below.

> [!SETTINGS]- [cache_enabled](#+minifier.js.cache_enabled){#+minifier.js.cache_enabled}
> Control if caching mechanism is enabled.

> [!SETTINGS]- [enabled](#+minifier.js.enabled){#+minifier.js.enabled}
> Control if JS minifier is enabled.

> [!SETTINGS]- [enabled_on_serve](#+minifier.js.enabled_on_serve){#+minifier.js.enabled_on_serve}
> Control if JS minifier is enabled while page is being served locally (mostly used for content creation).

> [!SETTINGS]- [exclude](#+minifier.js.exclude){#+minifier.js.exclude}
> Defines a list of exclusion patterns for files or directories that will not be minified.

> [!SETTINGS]- [exclude](#+minifier.js.extensions){#+minifier.js.extensions}
> Defines a list of file extensions that will be minified.

> [!SETTINGS]- [uglifyjs_path](#+minifier.js.uglifyjs_path){#+minifier.js.uglifyjs_path}
> Path to `uglifyjs` tool.

> [!SETTINGS]- [skip_minified](#+minifier.js.skip_minified){#+minifier.js.skip_minified}
> Skip files that are already minified (usually one with `.min.js` extension).
