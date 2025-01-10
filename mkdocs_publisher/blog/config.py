# MIT License
#
# Copyright (c) 2023-2025 Maciej 'maQ' Kusz <maciej.kusz@gmail.com>
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


class _BlogTranslationConfig(Config):
    teaser_link_text = option.Optional(option.Type(str))
    blog_page_title = option.Optional(option.Type(str))
    blog_navigation_name = option.Optional(option.Type(str))
    recent_blog_posts_navigation_name = option.Optional(option.Type(str))
    archive_page_title = option.Optional(option.Type(str))
    archive_navigation_name = option.Optional(option.Type(str))
    categories_page_title = option.Optional(option.Type(str))
    categories_navigation_name = option.Optional(option.Type(str))
    tags_page_title = option.Optional(option.Type(str))
    tags_navigation_name = option.Optional(option.Type(str))
    newer_posts = option.Optional(option.Type(str))
    older_posts = option.Optional(option.Type(str))


class _BlogCommentsConfig(Config):
    enabled = option.Type(bool, default=False)
    key_name = option.Type(str, default="comments")


class BlogPluginConfig(Config):
    # General settings
    lang = option.Choice(["en", "pl"], default="en")  # TODO: auto update based on files
    teaser_marker = option.Type(str, default="<!-- more -->")
    searchable_non_posts = option.Type(bool, default=False)
    posts_per_page = option.Type(int, default=5)
    slug = option.Type(str, default="blog")

    # Directories
    temp_dir = option.Type(str, default=".pub_blog_temp")
    blog_dir = option.Type(str, default="blog")
    archive_subdir = option.Type(str, default="archive")
    categories_subdir = option.Type(str, default="categories")
    tags_subdir = option.Type(str, default="tags")

    comments: _BlogCommentsConfig = option.SubConfig(_BlogCommentsConfig)  # type: ignore
    # Values that are in lang files and can be overriden
    translation: _BlogTranslationConfig = option.SubConfig(_BlogTranslationConfig)  # type: ignore
