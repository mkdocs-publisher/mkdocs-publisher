---
title: v1.4.0 - 2024-07-17
slug: v140
publish: true
date: 2024-07-16 17:53:18
update: 2024-07-17 20:24:28
tags:
  - v1.x
description: Publisher for MkDocs v1.4.0
categories:
  - release
---

Finally, I'm able to tell that [meta plugin](../03_setup/02_general/01_setting-up-meta.md) has some new features related to external linking and inner documents redirections. From now one, you can add a menu position that will be a [link](../03_setup/02_general/01_setting-up-meta.md#External%20links) to an external web page or add a file that will be just a [redirection](../03_setup/02_general/01_setting-up-meta.md#Redirections) to the other document.

There are also some bug fixes in the meta plugin related to publication status when using overview and for hidden pages. Now it should be working as intended. There are also small performance tweaks that can reduce generation time for bigger pages.

There is also a small update inside the social plugin for how titles are created [titles are created](../03_setup/03_seo_and_sharing/01_setting-up-social-cards.md#Title) in social cards. So far, title was just created based on `title` metadata, but in most cases other tools use a bit different approach. They create a title by joining title and site name, so it helps a bit a SEO stuff and site recognition (especially when there is no logo or site name in the image). From now one, this is a default behavior, but you have control over it [have control over it](../03_setup/03_seo_and_sharing/01_setting-up-social-cards.md#Site%20name%20in%20title).

In the very near future, there will be some big things happening to this project, like a new rewrite of the blog plugin, repository migration, documentation templates, project documentation reorganization and extension, the possibility to sponsor this project and insiders, etc. Stay tuned.

<!-- more -->

## Changelog

### :material-list-box: General

- ❎ extend overall code coverage
- ♻️ code refactor of some shared libraries

### :material-newspaper-variant-multiple: Blog

- ✅ blog post link title attribute

### :material-file-tree: Meta

- ❎ support for links and redirections
- ✅ overview pages doesn't respect publication status
- ✅ draft file in hidden directory is generated
- ✅ images link (remove hack fix)
- ♻️ code refactor in many places

### :material-share: Social

- ❎ site name is added to page title

---

> [!faq] Legend
> ❎ - added ✅ - fixed ♻️ - changed 🚫 - removed
