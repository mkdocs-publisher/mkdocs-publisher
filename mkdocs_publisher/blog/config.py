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

from mkdocs_publisher._shared.config_enums import PublishChoiceEnum
from mkdocs_publisher._shared.config_enums import SlugModeChoiceEnum


class _BlogTranslationConfig(Config):  # TODO: probably remove
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


class _BlogArchiveConfig(Config):
    enabled = option.Type(bool, default=False)
    slug = option.Type(str, default="archive")
    searchable = option.Type(bool, default=False)
    posts_per_page = option.Type(int, default=5)


class _BlogCategoriesConfig(Config):
    enabled = option.Type(bool, default=False)
    slug = option.Type(str, default="categories")
    searchable = option.Type(bool, default=False)
    key_name = option.Type(str, default="categories")
    warn_on_missing = option.Type(bool, default=True)
    posts_per_page = option.Type(int, default=5)


class _BlogCommentsConfig(Config):
    enabled = option.Type(bool, default=False)
    key_name = option.Type(str, default="comments")


class _BlogIndexConfig(Config):
    slug = option.Type(str, default="index")
    searchable = option.Type(bool, default=False)
    posts_per_page = option.Type(int, default=5)


class _BlogPostsConfig(Config):
    teaser_separator = option.Type(str, default="<!-- more -->")
    words_per_minute = option.Type(int, default=238)
    date_created_md_format = option.Type(str, default="%Y-%m-%d %H:%M:%S")
    date_created_display_format = option.Type(str, default="%Y.%m.%d %H:%M:%S")
    date_created_key_name = option.Type(str, default="date")
    date_updated_md_format = option.Type(str, default="%Y-%m-%d %H:%M:%S")
    date_updated_display_format = option.Type(str, default="%Y.%m.%d %H:%M:%S")
    date_updated_key_name = option.Type(str, default="update")
    slug = option.Type(str, default="posts")


class _BlogPublishConfig(Config):
    default = option.Choice(choices=PublishChoiceEnum.choices(), default=False)
    warn_on_missing = option.Type(bool, default=True)
    key_name = option.Type(str, default="publish")


class _BlogSlugConfig(Config):
    enabled = option.Type(bool, default=True)
    mode = option.Choice(choices=SlugModeChoiceEnum.choices(), default=SlugModeChoiceEnum.default())
    warn_on_missing = option.Type(bool, default=True)
    key_name = option.Type(str, default="slug")


class _BlogTagsConfig(Config):
    enabled = option.Type(bool, default=False)
    slug = option.Type(str, default="tags")
    searchable = option.Type(bool, default=False)
    key_name = option.Type(str, default="tags")
    warn_on_missing = option.Type(bool, default=True)
    posts_per_page = option.Type(int, default=5)


class _BlogTitleConfig(Config):
    key_name = option.Type(str, default="title")


class BlogPluginConfig(Config):
    blog_dir = option.Type(str, default="blog")
    blog_slug = option.Type(str, default="blog")

    archive: _BlogArchiveConfig = option.SubConfig(_BlogArchiveConfig)  # type: ignore[reportAssignmentType]
    categories: _BlogCategoriesConfig = option.SubConfig(_BlogCategoriesConfig)  # type: ignore[reportAssignmentType]
    comments: _BlogCommentsConfig = option.SubConfig(_BlogCommentsConfig)  # type: ignore[reportAssignmentType]
    index: _BlogIndexConfig = option.SubConfig(_BlogIndexConfig)  # type: ignore[reportAssignmentType]
    posts: _BlogPostsConfig = option.SubConfig(_BlogPostsConfig)  # type: ignore[reportAssignmentType]
    publish: _BlogPublishConfig = option.SubConfig(_BlogPublishConfig)  # type: ignore[reportAssignmentType]
    slug: _BlogSlugConfig = option.SubConfig(_BlogSlugConfig)  # type: ignore[reportAssignmentType]
    tags: _BlogTagsConfig = option.SubConfig(_BlogTagsConfig)  # type: ignore[reportAssignmentType]
    title: _BlogTitleConfig = option.SubConfig(_BlogTitleConfig)  # type: ignore[reportAssignmentType]
    # ==== Old below ====

    # General settings
    lang = option.Choice(["en", "pl"], default="en")  # TODO: auto update based on files
    teaser_marker = option.Type(str, default="<!-- more -->")
    searchable_non_posts = option.Type(bool, default=False)
    posts_per_page = option.Type(int, default=5)
    slug_old = option.Type(str, default="blog")

    # Directories
    temp_dir = option.Type(str, default=".pub_blog_temp")

    archive_subdir = option.Type(str, default="archive")
    categories_subdir = option.Type(str, default="categories")
    tags_subdir = option.Type(str, default="tags")

    # Values that are in lang files and can be overridden
    translation: _BlogTranslationConfig = option.SubConfig(_BlogTranslationConfig)  # type: ignore[reportAssignmentType]
