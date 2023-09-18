# MIT License
#
# Copyright (c) 2023 Maciej 'maQ' Kusz <maciej.kusz@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from mkdocs.config import config_options as option
from mkdocs.config.base import Config


class _MetaSlugConfig(Config):
    enabled = option.Type(bool, default=True)
    warn_on_missing = option.Type(bool, default=True)
    key_name = option.Type(str, default="slug")


class _MetaStatusConfig(Config):
    search_in_hidden = option.Type(bool, default=False)
    search_in_draft = option.Type(bool, default=False)
    file_default = option.Choice(choices=["draft", "hidden", "published"], default="draft")
    file_warn_on_missing = option.Type(bool, default=True)
    dir_default = option.Choice(choices=["draft", "hidden", "published"], default="published")
    dir_warn_on_missing = option.Type(bool, default=False)
    key_name = option.Type(str, default="visibility")


class _MetaTitleConfig(Config):
    key_name = option.Type(str, default="title")


class MetaPluginConfig(Config):
    dir_meta_file = option.Type(str, default="README.md")

    slug: _MetaSlugConfig = option.SubConfig(_MetaSlugConfig)  # type: ignore
    status: _MetaStatusConfig = option.SubConfig(_MetaStatusConfig)  # type: ignore
    title: _MetaTitleConfig = option.SubConfig(_MetaTitleConfig)  # type: ignore
