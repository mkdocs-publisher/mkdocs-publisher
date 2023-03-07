# mkdocs_publishing

[![PyPI version](https://badge.fury.io/py/mkdocs-blog-in.svg)](https://badge.fury.io/py/mkdocs-blog-in)
[![Github All Releases](https://img.shields.io/github/downloads/mkusz/mkdocs-blog-in/total.svg)]()

Blogging platform plugin for [MkDocs](https://www.mkdocs.org/).

## Another blogging plugin for MkDocs? But why?

The simplest answer is: because I couldn't find one good enough (and free).

The flip side of the same coin was that I wanted to migrate my personal blog related to [testing](https://testerembyc.pl) (sorry only in Polish, but you can try to use google translator) from [Nikola](https://getnikola.com/) that works quite well, but sometimes is overlly complicated, has almost none search functionality and markdown files are not the default one (but it's possible to use them). Why markdown format is so important? Becasue I love [Obsidian](https://obsidian.md) as a tool for gathering knowledge and this format is a crucial part of that tool.

At the time when this plugin was created, there was no free and qood alternatives. The only one that could be good enought was hidden behind a paid wall and was a part of a theme [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/blog/). Some of the ideas for this plugin and functionalities came from documentation of the Material for MkDocs theme, Nikola and other plugins.

Existing alternatives (with my comment):

- [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/blog/) - complex solution but paid,
- [mkdocs-blogging-plugin](https://github.com/liang2kl/mkdocs-blogging-plugin) - works, but very simple solution for very simple blog (limited tags usage, thame files modification neede, limited use of frontmatter, limited number of features),
- [mkdocs-blog-plugin](https://github.com/fmaida/mkdocs-blog-plugin) - no longer maintained and very simple,
- [python-mkblog](https://github.com/derJD/python-mkblog) - no longer maintained and very simple,
- [mkdocs-blog](https://github.com/andyoakley/mkdocs-blog) - no longer maintained and very simple,
- [material theme modification](https://www.dirigible.io/blogs/2021/11/2/material-blogging-capabilities/) - it's not a plugin, but comples theme modification, it's hard to extend and configure.

As you can see, there are just 2 still maintained plugins for blogging in MkDocs:
1. Material for MkDocs - complex but paid,
2. mkdosc-blogging-plugin - much simpler than Material for MkDocs.

At this moment (v0.4.0) of this plugin, it's functionality is somewhere in between those 2 (but closer to more complex solution). Since this is plugin that I will be using for my blog, it will be maintainted at least as long as my blog will be alive. I know that there is still a huge list of improvemnts I want to add (especially a documentation) but it's just a matter of time.

If you have an idea for some new functionality (or found a bug), please report and issue with a proper label.

> **Note**
> As a base for any development, mkdocs-material theme was used.

> **Warning**
> Consider this plugin as a beta, so before any use make sure you have a backup of your data.

If you have found any issue, have an idea for a feature, please submit an issue.

## Features

List of included features (more documentation is needed):

- automatic blog post index page generation with blog post teasers based on delimeter inside a blog post and own template (delimeter can be changed in plugin config in mkdocs.yaml),
- blog post/page update date based on blog post metadata,
- separate directory for blog post documents with auto generated separate navigation (blog posts are sorted from newest to oldest)
- home page set to blog post index with possibility to rename,
- auto adding link to full blog post from blog post index file (under each post that has teaser delimeter, if delimeter is not present, then full post is inside post index file, but is preserved in blog post navigation and site map).
- added sub pages for blog posts: archive, categories, tags

## How To

[TODO]

## Todo's

This list is unordered so functionalities can be added whenever in upcoming version:

- [ ] add cli tool for creating an empty blog posts and pages
- [ ] add templates overrides (same mechanism as in mkdocs-material theme) with cli tool to copy a template
- [ ] add social media preview (image metadata key to match RSS plugin defaults)
- [ ] add unittests
- [ ] add reading time
- [ ] add obsidian templates and preconfig for new vault
- [ ] add page/post meta to publish state like: draft, published, hidden
- [ ] add author/authors per page metadata (with predefined default in mkdocs.yaml)
- [ ] extend categories functionality like: possibility to add multiple categories (like tags), configurable limit of categories (with checks) and configurable list of categories
- [ ] add configurable date format
- [ ] file size optimization with cache
- [ ] create documentation
- [ ] documentation: integration with MkDocs RSS plugin
- [x] image optimization with cache
- [x] add concurrency in file optimization

## Image optimization

Image optimization is needed for optimal web speed loading that is needed for better scoring on search engines (part of propper SEO). The best image optimization that redeuce image file size but not image quality.

Since 2 most used image formats are PNG and JPEG, this plugin offers image optimization option. Tools used for image optimization were chosen to fulfill both main image optimization purposes: high quality with small file size.

### PNG

External tools:
- `pngquant` - image compression by color space manipulation
- `oxipng` - lossless compression optimizer

#### Why using both tools?

The reason is very simple. Both tools are operating in 2 different aspects of PNG image. `pngquant` reduce file size by reducing color palette to 8-bit with alpha channel and `oxipng` is optimizing image data compression algorithm without touching image data. Unfortunatelly there is no single tool that allows to perform both optimization.

#### Installation

- MacOS:

```commandline
brew install pngquant oxipng
```

### JPEG

```commandline

brew install mozjpeq

```

### SVG

```commandline

brew install svgo

```

### HTML, JS, CSS

For all of this files you have to have NPM already installed

```commandline

npm install -g html-minifier postcss cssnano postcss-svgo postcss-cli uglify-js

```

## Development

```commandline

poetry add --editable ../mkdocs-blog-in/

```


## Version history

### 0.4.0

- added: png image minifier (using: pngquant and oxipng)
- added: jpg image minifier (using: mozjpeg)
- added: svg image minifier (using: svgo)
- added: html file minifier (using: html-minifier)
- added: css file minifier (using: postcss with plugins: cssnano, svgo)
- added: js file minifier (using: uglifyjs)
- changed: internal file structure refactor with new global plugin config (BlogInConfig class) that will help with further development and small fixes and improvments
- fix: live reload infinite loop during `serve` caused by temporary files created and removed in blog directory
- change: project rename

### 0.3.0 - 2023.02.20

- fixed: for wrong directory structure in site-packages after install

### 0.2.0

- added: sub pages for archive, categories, blog
- added: configurable blog posts pagination with page navigation
- added: interface language change: EN and PL (help wanted with more languages)
- added: possibility to override for all interface text elements

### 0.1.0 - initial release

- added: blog post update date based on metadata
- added: blog post url link based on metadata
- added: blog post tags and categories based on metadata
- added: support for blog post teaser
- added: auto generation of blog posts navigation
