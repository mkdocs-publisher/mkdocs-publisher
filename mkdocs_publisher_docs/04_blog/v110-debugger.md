---
title: v1.1.0 - 2023-09-01
slug: v110
publish: published
date: 2023-09-01 11:50:56
update: 2023-09-01 14:38:45
tags:
  - v1.x
description: Publisher for MkDocs v1.1.0
categories:
  - release
icon: simple/obsidian
---

Here I am with a new version of Publisher for MkDocs plugins. I have promised to make smaller releases, but my brain is refusing me to work on a small scale. It's really hard to achieve that, especially when I started to have some feedback from you, users of this tool. Because of that feedback and some problems you encountered, I decided to focus in this release on 2 main topics: some bug fixing and introducing a new plugin called [pub-debugger](../02_setup/99_development/01_setting-up-debugger.md). This plugin allows for an insight into all messages produced by plugins while building (or serving) a web page. Also, it's able to produce a ZIP file, with some basic information that could help me, whenever you will need to report an [issue](https://github.com/mkusz/mkdocs-publisher/issues).

> [!WARNING] Privacy disclaimer
> `pub-debugger` plugin do not send any files over the internet, but if you want to use a Zip file as an attachment for an issue submission or share it with anybody, please make a review of the content of this archive file.
> > [!DANGER] Please remember
> > It's your data and your responsibility what you are publishing over the internet. This plugin is only giving you the tool that should help, and you cannot blame me (the author of this plugin) for any potential data leaks.

There is also one very crucial topic related to this project name. When I shared information about Publisher for MkDocs over an [official Obsidian.md community forum](https://forum.obsidian.md/top?period=daily) the developer of an Obsidian [GitHub Publisher plugin](https://github.com/ObsidianPublisher/obsidian-github-publisher) provided me information that we have some conflict related to our plugins name. We were also spoken privately over Discord and came to some agreement related to our work. More information can be found in [this thread](https://forum.obsidian.md/t/self-hosted-notes-by-using-mkdocs-with-blogging-capability/61643/6), but in short:

- My set of MkDocs plugins will be called **Publisher for MkDocs** since my work is related to MkDocs with additional support for Obsidian as an IDE/text editor,
- [Mara-Li](https://github.com/Lisandra-dev) Obsidian plugin will be called [GitHub Publisher](https://github.com/ObsidianPublisher/obsidian-github-publisher) since her work is related to Obsidian with the possibility to use MkDocs as a beck-end for publication.

In the feature, some elements of this project could be part of Mara-Li work, but it's her decision. I will continue working on this project and help her with some potential issues solving.

I have also spent some time on unification of look the setup documentation. Previously, documentation was created a similar way as Material for MkDocs is doing it, but I decided to drop this approach and simplify it a little bit. Most of the work was around configuration options, that was too verbose. Currently, all configuration options related to given functionality are gathered in a single code block with their default values, so it's easier to copy it to yours `mkdocs.yaml` file. As a result, all descriptions related to those options are placed below this code block, so it's easy to find the information about it. I hope it's now easier to navigate and understand all the configuration options.

A lot of you have been asking me about comparison to other tools and I have answered to them in this [Reddit thread](https://www.reddit.com/r/ObsidianMD/comments/149z9fe/mkdocs_publisher_as_an_alternative_for_official/). I have a plan to gather all this information and create a separate document about this (and also to some credits to projects I get inspiration from), but simply didn't have time for that so far.

There were also some requests related to the publication process. I'm aware that this is the biggest lacking right now of this project that is supposed to be related to publishing, and I will definitely solve this soon. There is an upcoming update related to that as:

- GitHub template repository,
- Docker image,
- GitHub Action,
- documentation.

I don't promise that all of the above will be ready in the next release, but some of them will be for sure.

<!-- more -->

## Changelog

### General

- :material-sync-circle: rename of directory with documentation files
- :material-sync-circle: Python libraries update
- :material-sync-circle: project naming unification
- :material-sync-circle: pre-commit JSON check and obsidian file exclusion
- :material-sync-circle: some links updates in documentation
- :material-sync-circle: code type hinting updates
- :material-sync-circle: logger names unification - [it's related to pub-debugger plugin](../02_setup/99_development/01_setting-up-debugger.md#python-logging-for-mkdocs)
- :material-sync-circle: code refactor and cleanup
- :material-minus-circle: drop `python-frontmatter` from Python libraries

### Blog

- :material-check-circle: minor fix for internal linking (still not full solution)
- :material-sync-circle: fix for deprecated warning regarding `importlib.resources`

### Minifier

- :material-sync-circle: small code reformat related to shared library changes
- :material-sync-circle: files are not minified when using `mkdocs serve` (this is default behavior, but it can be changed)

### Meta

- :material-plus-circle: possibility to declare whole directory as hidden
- :material-plus-circle: more logging messages
- :material-plus-circle: better support for `pub-obsidian` plugin (template and obsidian directory are now always drafts)
- :material-check-circle: fix for error with reading `README.md` when no empty line at the end of file
- :material-check-circle: fix for adding again the same directory to draft directories when using `mkdocs serve`

### Obsidian

- :material-check-circle: minor fix for internal linking (still not full fix)
- :material-check-circle: fix for preserving new line in callouts

### Debugger (new plugin)

- :material-plus-circle: console log reformatting with configuration
- :material-plus-circle: added logging into `*.log` file with configuration
- :material-plus-circle: added old log file replacement
- :material-plus-circle: ZIP file creation with log output and some additional files

---

> [!info] Legend
> :material-plus-circle: - added
>
> :material-minus-circle: - removed
>
> :material-check-circle: - fixed
>
> :material-sync-circle: - changed
