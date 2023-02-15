import logging
from collections import OrderedDict
from datetime import datetime
from pathlib import Path
from typing import Dict

from mkdocs.structure.files import Files
from mkdocs.structure.nav import Navigation
from mkdocs.structure.nav import Section
from mkdocs.structure.pages import Page

from src.plugin.config import BlogInPluginConfig
from src.plugin.structures import BlogPost

log = logging.getLogger("mkdocs.plugins.blog-in")


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
    blog_posts: Dict[datetime, BlogPost],
    config_nav: OrderedDict,
    posts_dir: Path,
):
    """Reorder blog posts in config navigation section from newest to oldest."""

    log.info("Reorder blog posts from newest to oldest")
    config_nav[str(posts_dir).title()] = []
    for date in sorted(blog_posts, reverse=True):
        config_nav[str(posts_dir).title()].append({blog_posts[date].title: blog_posts[date].path})


def blog_post_nav_remove(
    nav: Navigation,
    blog_posts: str,
    config: BlogInPluginConfig,
) -> None:
    """Remove blog posts pages and section from direct navigation."""

    log.info("Remove blog posts pages and section from direct navigation")
    nav.items = [
        i for i in nav.items if not (isinstance(i, Section) and i.title.lower() == blog_posts)
    ]

    log.info("Remove blog index from navigation menu")
    for item in nav.items:
        if isinstance(item, Section) and item.title == config.index_name:
            children = []
            for section_item in item.children:
                if not (
                    isinstance(section_item, Page) and str(section_item.title).startswith("index-")
                ):
                    children.append(section_item)
            item.children = children
