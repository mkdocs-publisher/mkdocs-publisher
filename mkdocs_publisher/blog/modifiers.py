import logging
from collections import OrderedDict
from copy import deepcopy
from typing import cast

from mkdocs.structure.files import Files
from mkdocs.structure.nav import Navigation
from mkdocs.structure.nav import Section
from mkdocs.structure.pages import Page

from mkdocs_publisher.blog.structures import BlogConfig

log = logging.getLogger("mkdocs.plugins.publisher.blog")


def blog_post_slug_modifier(blog_config: BlogConfig, files: Files) -> Files:
    """Modify File object destination file paths and url to defined blog post slug."""

    blog_posts = {post.path: post for post in blog_config.blog_posts.values()}  # type: ignore
    new_files = Files([])

    log.info("Modify blog posts url addresses based on slug")
    for file in files:
        if file.src_uri in blog_posts and blog_posts[file.src_uri].slug is not None:
            url = file.url.split("/")
            url[-1] = blog_posts[file.src_uri].slug  # type: ignore
            file.url = f"{'/'.join(url)}/"
            file.name = str(blog_posts[file.src_uri].slug)
            url.append(file.dest_uri.split("/")[-1])
            file.dest_uri = "/".join(url)
            file.abs_dest_path = str(blog_config.site_dir / file.dest_uri)
            log.debug(f"Blog post: {blog_posts[file.src_uri].title} url is: {file.url}")
        new_files.append(file)

    return new_files


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
    nav.items = [
        i for i in nav.items if not (isinstance(i, Section) and i.title.lower() == "_blog_posts_")
    ]
    log.info("Removing blog sub index pages from navigation menu")
    for item in nav.items:
        if (
            isinstance(item, Section)
            and item.title == blog_config.translation.blog_navigation_name
        ):
            children = []
            for section_item in item.children:
                if not (
                    isinstance(section_item, Page) and str(section_item.title).startswith("index-")
                ):
                    children.append(section_item)
                if (
                    isinstance(section_item, Page)
                    and not start_page
                    and str(section_item.title).startswith("index-0")
                ):
                    children.append(section_item)
            item.children = children


def blog_post_nav_next_prev_change(start_page: bool, blog_config: BlogConfig, page: Page):
    """Change blog post next/prev navigation"""

    if (start_page and page.title == "index") or (not start_page and page.title == "index-0"):
        page.title = blog_config.translation.recent_blog_posts_navigation_name
        if page.next_page is not None and str(page.next_page.title).startswith("index-"):
            next_page_copy = cast(Page, deepcopy(page.next_page))
            next_page_copy.title = blog_config.translation.older_posts
            page.next_page = next_page_copy
    elif str(page.title).startswith("index") or (
        page.previous_page is not None and str(page.previous_page.title).startswith("index")
    ):
        page.title = blog_config.translation.older_posts
        previous_page_copy = cast(Page, deepcopy(page.previous_page))
        previous_page_copy.title = blog_config.translation.newer_posts
        page.previous_page = previous_page_copy
        if page.next_page is not None and str(page.next_page.title).startswith("index-"):
            next_page_copy = cast(Page, deepcopy(page.next_page))
            next_page_copy.title = blog_config.translation.older_posts
            page.next_page = next_page_copy
