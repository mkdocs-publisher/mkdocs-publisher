import logging
from collections import OrderedDict
from datetime import datetime
from pathlib import Path
from typing import Dict

from mkdocs.structure.files import Files
from mkdocs.structure.nav import Navigation
from mkdocs.structure.nav import Section
from mkdocs.structure.pages import Page

from src.structures import BlogPost

log = logging.getLogger(f"mkdocs.plugins.{__name__}")


def blog_post_slug_modifier(
    blog_posts: Dict[datetime, BlogPost], files: Files, site_dir: Path
) -> Files:
    """Modify File object destination file paths and url to defined blog post slug."""

    blog_posts = {post.path: post for post in blog_posts.values()}  # type: ignore
    new_files = Files([])

    log.info("Modify blog posts url addresses based on slug")
    for file in files:
        if file.src_uri in blog_posts and blog_posts[file.src_uri].slug is not None:
            slug = blog_posts[file.src_uri].slug
            file.name = slug.split("/")[-1]  # type: ignore
            file.url = f"{slug}/"
            file.dest_uri = f"{slug}/index.html"
            file.abs_dest_path = str(site_dir / file.dest_uri)
            log.debug(f"Blog post: {blog_posts[file.src_uri].title} url is: {file.url}")
        new_files.append(file)

    return new_files


def blog_post_nav_sorter(
    blog_posts: Dict[datetime, BlogPost], config_nav: OrderedDict, posts_dir: Path
):
    """Reorder blog posts in config navigation section from newest to oldest."""

    log.info("Reorder blog posts from newest to oldest")
    config_nav[str(posts_dir).title()] = []
    for date in sorted(blog_posts, reverse=True):
        config_nav[str(posts_dir).title()].append({blog_posts[date].title: blog_posts[date].path})


def blog_post_nav_remove(
    nav: Navigation,
    posts_dir: str,
) -> None:
    """Remove blog posts pages and section from direct navigation."""

    log.info("Remove blog posts pages and section from direct navigation")
    nav.pages = [p for p in nav.pages if not p.file.src_uri.startswith(posts_dir)]

    nav.items = [
        i for i in nav.items if not (isinstance(i, Section) and i.title.lower() == posts_dir)
    ]


def prev_next_link_remove(
    page: Page, blog_posts: Dict[datetime, BlogPost], posts_index_files: Dict[str, Path]
):
    """Remove next/prev page links from given pages."""
    index_files_titles = posts_index_files.keys()
    blog_posts_titles = [blog_posts[date].title for date in sorted(blog_posts, reverse=True)]

    prev_pages_list = [max(index_files_titles), blog_posts_titles[0]]
    next_pages_list = [min(index_files_titles), blog_posts_titles[-1]]

    if page.title in prev_pages_list:
        page.previous_page = None
    elif page.title in next_pages_list:
        page.next_page = None
