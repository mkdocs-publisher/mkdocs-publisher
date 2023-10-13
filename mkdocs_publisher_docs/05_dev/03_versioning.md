---
title: Versioning
icon: octicons/number-24
slug: versioning
publish: published
date: 2023-03-30 13:12:26
update: 2023-10-12 23:53:46
description: Approach to versioning
categories:
  - general
  - versioning
---

# Approach to versioning

The current approach to versioning of _“Publisher for MkDocs”_ is based on [semantic versioning](https://semver.org) and looks like this `v1.2.3`, or in general, it's: `vMAJOR,MINOR,PATCH` where:

- `MAJOR` number is increased when a new braking changes are introduced, for example some settings are removed or MkDocs is updated, and this project has to adjust to those changes.
- `MINOR` number is increased when new functionality is introduced without breaking changes or a new plugin is added.
- `PATCH` number is increased when there is no new functionality and usually is used for bug fixes. It can also be used for
