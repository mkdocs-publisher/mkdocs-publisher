import importlib.resources
import logging
from collections import OrderedDict
from datetime import datetime
from pathlib import Path
from typing import Dict
from typing import cast

import frontmatter
import jinja2

from src import templates
from src.plugin.config import BlogInPluginConfig
from src.plugin.structures import BlogPost

log = logging.getLogger("mkdocs.plugins.blog-in")


def create_blog_post_pages(
    blog_posts: Dict[datetime, BlogPost],
    temp_files: Dict[str, Path],
    config_nav: OrderedDict,
    docs_dir: Path,
    config: BlogInPluginConfig,
) -> None:
    """Create blog posts index files."""

    # TODO: Add templates from override
    # TODO: This file needs some serious refactor and cleanup

    # templates = jinja2.Environment(loader=jinja2.FileSystemLoader("templates/"))
    # print(templates.list_templates())
    # template = templates.get_template("index.html")
    log.info("Creating blog posts index files")

    posts_chunks: Dict[str, list] = {}
    archive_chunks: Dict[str, list] = {}
    categories_chunks: Dict[str, list] = {}
    tags_chunks: Dict[str, list] = {}

    # Build post pages
    for index, date in enumerate(sorted(blog_posts, reverse=True)):
        index = (
            "index"
            if index < config.posts_per_page
            else f"index-{str(index//config.posts_per_page)}"
        )
        if index not in posts_chunks:
            posts_chunks[index] = []
        posts_chunks[index].append(blog_posts[date])

    # Build archive, category and tag pages
    for date in sorted(blog_posts, reverse=True):
        date: datetime
        year = str(date.year)
        if year not in archive_chunks:
            archive_chunks[year] = []
        archive_chunks[year].append(blog_posts[date].as_dict)

        category = cast(str, blog_posts[date].category)
        if category not in categories_chunks:
            categories_chunks[category] = []
        categories_chunks[category].append(blog_posts[date].as_dict)

        tags = cast(list, blog_posts[date].tags)
        for tag in tags:
            if tag not in tags_chunks:
                tag = tag.replace("/", "-")
                tags_chunks[tag] = []
            tags_chunks[tag].append(blog_posts[date].as_dict)

    # Reorder categories alphabetically
    categories_chunks = {cat: categories_chunks[cat] for cat in sorted(categories_chunks)}

    # Reorder tags alphabetically
    tags_chunks = {tag: tags_chunks[tag] for tag in sorted(tags_chunks)}

    config_nav[config.index_name] = {}

    for key, single_posts_chunk in posts_chunks.items():
        file_name = f"{key}.md"
        file_path = docs_dir / file_name

        _render_and_write_page(
            single_posts_chunk=single_posts_chunk,
            file_path=file_path,
            config=config,
            page_title="Blog",  # TODO: make it config value
        )

        temp_files[f"{config.index_name}/{key}"] = file_path
        log.debug(f"Creating blog post chunk file: {file_path}")

        config_nav[config.index_name][key] = f"{file_name}"

    _create_pages(
        posts_chunks=categories_chunks,
        temp_files=temp_files,
        config_nav=config_nav[config.index_name],
        docs_dir=docs_dir,
        sub_dir=Path(config.categories_dir),
        sub_dir_name=config.categories_name,
        config=config,
    )

    _create_pages(
        posts_chunks=tags_chunks,
        temp_files=temp_files,
        config_nav=config_nav[config.index_name],
        docs_dir=docs_dir,
        sub_dir=Path(config.tags_dir),
        sub_dir_name=config.tags_name,
        config=config,
    )

    _create_pages(
        posts_chunks=archive_chunks,
        temp_files=temp_files,
        config_nav=config_nav[config.index_name],
        docs_dir=docs_dir,
        sub_dir=Path(config.archive_dir),
        sub_dir_name=config.archive_name,
        config=config,
    )


def _create_pages(
    posts_chunks: Dict[str, list],
    temp_files: Dict[str, Path],
    config_nav: OrderedDict,
    docs_dir: Path,
    sub_dir: Path,
    sub_dir_name: str,
    config: BlogInPluginConfig,
):
    config_nav[sub_dir_name] = {}

    pages_dir = docs_dir / config.posts_dir / sub_dir

    if not pages_dir.exists():
        pages_dir.mkdir()

    for key, single_posts_chunk in posts_chunks.items():
        file_name = f"{key}.md"
        file_path = pages_dir / file_name

        _render_and_write_page(
            single_posts_chunk=single_posts_chunk,
            file_path=file_path,
            config=config,
            page_title=f"{sub_dir_name} - {key}",
        )

        temp_files[f"{sub_dir_name}/{key}"] = file_path
        log.debug(f"Creating blog post chunk file: {file_path}")

        config_nav[sub_dir_name][key] = f"{config.posts_dir}/{sub_dir}/{file_name}"


def _render_and_write_page(
    single_posts_chunk: list,
    file_path: Path,
    config: BlogInPluginConfig,
    page_title: str,
):
    index_template = importlib.resources.read_text(templates, "posts-list.html")

    context = {
        "posts": single_posts_chunk,
        "config": config,
    }
    template = jinja2.Environment(loader=jinja2.BaseLoader()).from_string(index_template)

    page = frontmatter.Post(content=template.render(context))
    page["title"] = page_title

    with open(file_path, mode="wb") as teasers_index:
        frontmatter.dump(page, teasers_index)
