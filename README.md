# mkdocs-blogger
This plugin change behaviour of MkDocs, so it allows to use it as a blogging platform.

> **Note**
> As a base for any development, mkdocs-material theme was used.

> **Warning**
> Consider this plugin as a beta, so before any use make sure you have a backup of your data.

If you have found any issue, have an idea for a feature, please submit an issue.

## Features

List of included features (more documentation is needed):

- automatic blog post index page generation with blog post teasers based on delimeter inside a blog post and own template (delimeter can be changed in plugin config in mkdocs.yaml),
- blog post update date based on blog post metadata,
- separate directory for blog post documents with auto generated separate navigation (blog posts are sorted from newest to oldest)
- home page set to blog post index with possibility to rename,
- auto adding link to full blog post from blog post index file (under each post that has teaser delimeter, if delimeter is not present, then full post is inside post index file, but is preserved in blog post navigation and site map).

## How To

[TODO]

## Todo's

- [ ] add cli tool for creating an empty blog post and page
- [ ] add sub pages for categories
- [ ] add sub pages for tags
- [ ] add templates overrides (same mechanism as in mkdocs-material theme)
- [ ] add social media preview

## Version history

### 0.1.0

- initial release
