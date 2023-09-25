---
title: Versioning
slug: versioning
publish: published
date: 2023-03-30 13:12:26
update: 2023-08-01 12:00:53
description: Approach to versioning
categories:
  - general
  - versioning
---

# Approach to versioning

The current approach to versioning of _“Publisher for MkDocs”_ is based on [semantic versioning](https://semver.org) and looks like this `v1.2.3`, or in general, it's: `vMAJOR,MINOR,PATCH` where:

- `MAJOR` number is increased when a new braking API change is introduced,
- `MINOR` number is increased when new functionality is introduced without API changes,
- `PATCH` number is increased when there is no new functionality and usually is used for bug fixes.

Because this package is based on MkDocs API, the only reason to change `MAJOR` number would be to break compatibility with an older version of MkDocs or when this package will go out of beta stage.

Since this package contains various sets of plugins, `MINOR` number will be changed when a new plugin is introduced or an existing one changes significantly (new config options, new functionality added, etc.).

`PATCH` number will be used mostly for bug fixes and smaller internal changes like documentation modifications, code refactor or unit testing changes.
