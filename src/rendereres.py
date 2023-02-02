import importlib.resources
import logging
from collections import OrderedDict
from datetime import datetime
from pathlib import Path
from typing import Dict
from typing import Union

import jinja2

from src import templates
from src.structures import BlogPost

log = logging.getLogger(f"mkdocs.plugins.{__name__}")


def create_blog_post_index_pages(
    blog_posts: Dict[datetime, BlogPost],
    posts_index_files: Dict[str, Path],
    config_nav: OrderedDict,
    docs_dir: Path,
    teaser_link_text: str,
    index_name: str,
) -> None:
    """Create blog posts index files."""

    # TODO: Add templates from override

    # templates = jinja2.Environment(loader=jinja2.FileSystemLoader("templates/"))
    # print(templates.list_templates())
    # template = templates.get_template("index.html")
    log.info("Creating blog posts index files")
    index_template = importlib.resources.read_text(templates, "posts-list.html")

    posts_chunks: Dict[str, list] = {}
    for date in sorted(blog_posts, reverse=True):
        date: datetime
        year = str(date.year)
        if year not in posts_chunks:
            posts_chunks[year] = []
        posts_chunks[year].append(blog_posts[date].as_dict)

    config_nav[index_name] = {}

    index_year: Union[str, None] = None
    for year, single_posts_chunk in posts_chunks.items():
        post_index_file_name = f"{year}.md"
        if index_year is None:
            index_year = year
            post_index_file_name = "index.md"
        post_index_file = docs_dir / post_index_file_name
        context = {
            "posts": single_posts_chunk,
            "teaser_link_text": teaser_link_text,
        }
        template = jinja2.Environment(loader=jinja2.BaseLoader()).from_string(index_template)

        with open(post_index_file, mode="w", encoding="utf-8") as teasers_index:
            teasers_index.write(template.render(context))
        posts_index_files[year] = post_index_file
        log.debug(f"Creating post index file: {post_index_file}")

        config_nav[index_name][year] = post_index_file_name
