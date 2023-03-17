# Version history

### 0.4.0

General:

- changed: project rename
- added: cross configuration of blog and auto-nav plugins:
  - blog do not add auto-nav meta files
  - auto-nav automatically adds blog dir to skipped directories since it will be build by blog
  - if one of the plugins is not enabled, other is not using it's values

Blog:

- added: possibility to choose a blog as a starting page with option to define manually blog in nav configuration
- added: `slug` config option for setting an entire blog main directory url
- changed: internal file structure refactor with new global plugin config (BlogConfig class) that will help with further development with small fixes and improvements
- changed: blog subdirectory navigation creation (entry path needs to be equal to ssubdirectory name)
- fixed: live reload infinite loop during `serve` caused by temporary files created and removed in blog directory
- fixed: navigation is no longer overriden by a blog (if there is no other nav, blog will create on with recent posts as a main page)

Minifier (new plugin):

- added: png image minifier (using: pngquant and oxipng)
- added: jpg image minifier (using: mozjpeg)
- added: svg image minifier (using: svgo)
- added: html file minifier (using: html-minifier)
- added: css file minifier (using: postcss with plugins: cssnano, svgo)
- added: js file minifier (using: uglifyjs)

Auto-nav (new plugin):

- added: build navigation based on file names
- added: directory metadata and additional settings can be set in a frontmatter of `*.md` file (default to `README.md`)
- added: configuration of sort prefix delimiter
- added: sort prefix removal in url and site files

### 0.3.0 - 2023.02.20

- fixed: for wrong directory structure in site-packages after install

### 0.2.0 - 2023.02.19

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
