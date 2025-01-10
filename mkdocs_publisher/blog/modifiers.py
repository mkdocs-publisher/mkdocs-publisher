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

import logging
from collections import OrderedDict
from copy import deepcopy
from typing import Optional

from mkdocs.structure.nav import Navigation
from mkdocs.structure.nav import Section
from mkdocs.structure.pages import Page

from mkdocs_publisher.blog.structures import BlogConfig

log = logging.getLogger("mkdocs.publisher.blog.modifiers")


def blog_post_nav_sorter(
    blog_config: BlogConfig,
    config_nav: OrderedDict,
):
    """Reorder blog posts in config navigation section from newest to oldest."""
    log.info("Reorder blog posts from newest to oldest")
    config_nav["_blog_posts_"] = [
        {blog_config.blog_posts[date].title: blog_config.blog_posts[date].path}
        for date in sorted(blog_config.blog_posts, reverse=True)
    ]


def blog_post_nav_remove(
    start_page: bool,
    blog_config: BlogConfig,
    nav: Navigation,
) -> None:
    """Remove blog posts pages, subindexes and section from direct navigation."""

    log.info("Removing blog posts pages and section from direct navigation")
    nav.items = [i for i in nav.items if not (isinstance(i, Section) and i.title.lower() == "_blog_posts_")]
    log.info("Removing blog sub index pages from navigation menu")
    for item in nav.items:
        if isinstance(item, Section) and item.title == blog_config.translation.blog_navigation_name:
            children = []
            for section_item in item.children:
                if not (isinstance(section_item, Page) and str(section_item.title).startswith("index-")):
                    children.append(section_item)
                if isinstance(section_item, Page) and not start_page and str(section_item.title).startswith("index-0"):
                    children.append(section_item)
            item.children = children


def blog_post_nav_next_prev_change(start_page: bool, blog_config: BlogConfig, page: Page):
    """Change blog post next/prev navigation"""

    if (start_page and page.title == "index") or (not start_page and page.title == "index-0"):
        page.title = blog_config.translation.recent_blog_posts_navigation_name  # type: ignore
        if page.next_page is not None and str(page.next_page.title).startswith("index-"):
            next_page_copy: Page = deepcopy(page.next_page)
            next_page_copy.title = blog_config.translation.older_posts  # type: ignore
            page.next_page = next_page_copy
    elif str(page.title).startswith("index") or (
        page.previous_page is not None and str(page.previous_page.title).startswith("index")
    ):
        page.title = blog_config.translation.older_posts  # type: ignore
        previous_page_copy: Optional[Page] = deepcopy(page.previous_page)
        previous_page_copy.title = blog_config.translation.newer_posts  # type: ignore
        page.previous_page = previous_page_copy
        if page.next_page is not None and str(page.next_page.title).startswith("index-"):
            next_page_copy: Page = deepcopy(page.next_page)
            next_page_copy.title = blog_config.translation.older_posts  # type: ignore
            page.next_page = next_page_copy
