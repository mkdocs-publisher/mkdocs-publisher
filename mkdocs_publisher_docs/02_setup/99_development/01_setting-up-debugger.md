---
title: Setting up debugger
slug: pub-debugger
status: draft
date: 2023-08-01 11:49:05
update: 2023-08-19 23:13:41
description: Setting up a Publisher for MkDocs debugger plugin for development purposes
categories:
  - plugin
  - debugger
---

# Setting up a debugger plugin

## Introduction

Each good developer knows, how important is the possibility to read proper logs from running application when there is some issue. MkDocs by default produces some logs while documentation is being built or while the built-in server is running. Because the whole MkDocs is written using the Python programming language, there is a possibility to configure a debugger in tools like PyCharm or VsCode. But how to handle logging when you are just a user and do not have a needed knowledge and just want to submit an issue because you have found some problem? To help with debugging by logging and producing additional files that can be attached to the issue submission, Publisher for MkDocs contains a `pub-debugger` plugin. It's built with 3 main modules:

- [console logger](#Logging%20to%20the%20console) that allows to change the output produced to the console,
- [file logger](#Logging%20to%20the%20file) that allows to produce the log file,
- [Zip file generator](#Generating%20Zip%20file) that allows to produce a Zip file with log file produced by previous module and some additional files like `mkdocs.yml` and Python package files like `requirements.txt` or `pyproject.tml` and `poetry.lock` (depends on type of Python package manager you have used).

> [!INFO] Console and file logger settings
> Both console and file loggers are configured separately and their defaults settings are different.

> [!WARNING] Privacy disclaimer
> `pub-debugger` plugin do not send any files over the internet, but if you want to use a Zip file as an attachment for an issue submission or share it with anybody, before please make a review of the content of this archive file.
> > [!DANGER] Please remember
> > It's your data and your responsibility what you are publishing over the internet. This plugin is only giving you the tool that should help, and you cannot blame me (the author of this plugin) for any potential data leaks.

## Python logging for MkDocs

> [!INFO] Information
> This section is for any MkDocs plugin developer.

Because MkDocs is written in Python, whenever someone wants to write a new plugin and see some information during documentation build, he has to use a [logging library](https://docs.python.org/3/library/logging.html). The usual use of this library is to do something like this:

===+ ":octicons-file-code-16: new_mkdocs_plugin.py"

```python hl_lines="3-4"
import logging

logger = logging.get_logger(__name__)
logger.info("Some output")
```

The biggest problem with this approach is that `__name__` becomes a file name (without extension), so the logger for the above example is `new_mkdocs_plugin`. Since all loggers inside MkDocs have a name corresponding to a directory structure that leads to the file where logger is used, any MkDocs plugin developer should do the same.


> [!TIP] The best practice for logger naming
> Logger name should be built according to given structure:
> `mkdocs.plugins.[project_name].[directory].[optional_sub_directories].[file_name]`.

Let's take a look at [one of the files from this project repository](https://github.com/mkusz/mkdocs-publisher/blob/main/mkdocs_publisher/minifier/minifiers.py).

===+ ":octicons-file-code-16: minifier.py"

	```python hl_lines="5"
	import logging

	...

	log = logging.getLogger("mkdocs.plugins.publisher.minifier.minifiers")
	```

=== ":fontawesome-solid-folder-tree:"

	```console hl_lines="1-4"
	.
	└─ mkdocs_publisher/
	  └─ minifier/
		└─ minifiers.py
	```



##  Configuration

To enable the built-in debugger plugin, the following lines have to be added to `mkdocs.yml` file:

===+ ":octicons-file-code-16: mkdocs.yml"

    ```yaml hl_lines="2"
    plugins:
      - pub-debugger
    ```

### Console logging



![](../../_attachments/debugger_console_example.png)

### File logging



### Zip file generation
