# Plans for future development

## Plugins

### Blog

- [ ] Add: blog post reading time + watch time (defined in post meta)
- [ ] Add: possibility to disable categories and/or tags pages
- [ ] Add: automatic add [search exclude](https://squidfunk.github.io/mkdocs-material/setup/setting-up-site-search/#search-exclusion) to draft and hidden pages when using material for MkDocs theme with search plugin enabled
- [ ] Add: authors and update date in the template
- [ ] Add: blog posts index template override
- [ ] Add: language override in YAML file
- [ ] Add: configurable date format
- [ ] Add: blog post publication state: draft, published, hidden
- [ ] Fix: `blog` slug do not open first page when not in standalone mode

### Minifier

- [ ] Add: ignored files list/pattern
- [ ] Add: stats for number of minified/taken from cache files

### Meta-apply (new plugin)

- [ ] Add: usage of page frontmatter
- [ ] Add: document publication state: draft, published, hidden
- [ ] Add: sitemap optimizations and creation of `robots.txt` file based on document status

### Social (new plugin)

- [ ] Add: inject social media preview into document based on frontmatter

### Obsidian (new plugin)

- [ ] Add: callout format support
- [ ] Add: wiki links format support
- [ ] Add: charts
- [ ] Add: mindmaps (???)
- [ ] Add: templates (blog post, page, etc.)
- [ ] Add: backlinks
- [ ] Add: graphs (long term goal)

## General

### CLI tool

- [ ] Add: project initialization that preconfigure `mkdocs.yml`
- [ ] Add: create a new blog post
- [ ] Add: document/blog post slug update
- [ ] Add: check for minifier tools
- [ ] Add: minify single file using minifier
- [ ] Add: document/blog post publication state change

### Documentation

- [ ] Blog plugin
- [ ] Minifier plugin
- [ ] Auto-nav plugin
- [ ] Integration with RSS plugin
- [ ] How to set up and use docker image
- [ ] Setting up CI/CD in GitHub Actions
- [ ] This plugin development how to

### Other

 - [ ] Create Docker image with everything preinstalled and preconfigured
 - [ ] GitHub repo with preconfigured pages, etc. (can be integrated with Docker Image creation)
 - [ ] Unittests and code coverage with pre-commit
 - [ ] Cleanup list of code TODO's
 - [ ] Drop `python-frontmatter` for MkDocs built-in library for metadata retirval
