import importlib.resources
import logging
from collections import OrderedDict
from datetime import datetime
from pathlib import Path
from typing import Dict
from typing import cast

import frontmatter
import jinja2

from mkdocs_blog_in import templates
from mkdocs_blog_in.structures import BlogConfig

log = logging.getLogger("mkdocs.plugins.blog-in")


def create_blog_post_pages(
    blog_config: BlogConfig,
    config_nav: OrderedDict,
) -> None:
    """Create blog posts index files."""

    log.info("Creating blog posts index files")

    posts_chunks: Dict[str, list] = {}
    archive_chunks: Dict[str, list] = {}
    categories_chunks: Dict[str, list] = {}
    tags_chunks: Dict[str, list] = {}

    # Build post pages
    for index, date in enumerate(sorted(blog_config.blog_posts, reverse=True)):
        index = (
            "index"
            if index < blog_config.plugin_config.posts_per_page
            else f"index-{str(index//blog_config.plugin_config.posts_per_page)}"
        )
        if index not in posts_chunks:
            posts_chunks[index] = []
        posts_chunks[index].append(blog_config.blog_posts[date])

    # Build archive, category and tag pages
    for date in sorted(blog_config.blog_posts, reverse=True):
        date: datetime
        year = str(date.year)
        if year not in archive_chunks:
            archive_chunks[year] = []
        archive_chunks[year].append(blog_config.blog_posts[date].as_dict)

        category = cast(str, blog_config.blog_posts[date].category)
        if category not in categories_chunks:
            categories_chunks[category] = []
        categories_chunks[category].append(blog_config.blog_posts[date].as_dict)

        tags = cast(list, blog_config.blog_posts[date].tags)
        for tag in tags:
            if tag not in tags_chunks:
                tag = tag.replace("/", "-")
                tags_chunks[tag] = []
            tags_chunks[tag].append(blog_config.blog_posts[date].as_dict)

    # Reorder categories alphabetically
    categories_chunks = {cat: categories_chunks[cat] for cat in sorted(categories_chunks)}

    # Reorder tags alphabetically
    tags_chunks = {tag: tags_chunks[tag] for tag in sorted(tags_chunks)}
    config_nav[blog_config.translation.blog_navigation_name] = {}

    for key, single_posts_chunk in posts_chunks.items():
        file_name = f"{key}.md"
        file_path = blog_config.docs_dir / file_name

        _render_and_write_page(
            single_posts_chunk=single_posts_chunk,
            file_path=file_path,
            blog_config=blog_config,
            page_title=blog_config.translation.blog_page_title,
        )

        blog_config.temp_files[f"{blog_config.translation.blog_navigation_name}/{key}"] = file_path
        log.debug(f"Creating blog post chunk file: {file_path}")

        config_nav[blog_config.translation.blog_navigation_name][key] = f"{file_name}"

    _create_pages(
        blog_config=blog_config,
        posts_chunks=archive_chunks,
        config_nav=config_nav[blog_config.translation.blog_navigation_name],
        sub_dir=Path(blog_config.plugin_config.archive_subdir),
        navigation_name=blog_config.translation.archive_navigation_name,
        page_title=blog_config.translation.archive_page_title,
    )

    _create_pages(
        blog_config=blog_config,
        posts_chunks=categories_chunks,
        config_nav=config_nav[blog_config.translation.blog_navigation_name],
        sub_dir=Path(blog_config.plugin_config.categories_subdir),
        navigation_name=blog_config.translation.categories_navigation_name,
        page_title=blog_config.translation.categories_page_title,
    )

    _create_pages(
        blog_config=blog_config,
        posts_chunks=tags_chunks,
        config_nav=config_nav[blog_config.translation.blog_navigation_name],
        sub_dir=Path(blog_config.plugin_config.tags_subdir),
        navigation_name=blog_config.translation.tags_navigation_name,
        page_title=blog_config.translation.tags_page_title,
    )


def _create_pages(
    blog_config: BlogConfig,
    posts_chunks: Dict[str, list],
    config_nav: OrderedDict,
    sub_dir: Path,
    navigation_name: str,
    page_title: str,
):
    config_nav[navigation_name] = {}

    pages_dir = blog_config.docs_dir / blog_config.blog_dir / sub_dir

    if not pages_dir.exists():
        pages_dir.mkdir()

    for key, single_posts_chunk in posts_chunks.items():
        file_name = f"{key}.md"
        file_path = pages_dir / file_name

        _render_and_write_page(
            single_posts_chunk=single_posts_chunk,
            file_path=file_path,
            blog_config=blog_config,
            page_title=f"{page_title} - {key}",
        )

        blog_config.temp_files[f"{sub_dir}/{key}"] = file_path
        log.debug(f"Creating blog post chunk file: {file_path}")

        config_nav[navigation_name][key] = f"{blog_config.blog_dir}/{sub_dir}/{file_name}"


def _render_and_write_page(
    single_posts_chunk: list,
    file_path: Path,
    blog_config: BlogConfig,
    page_title: str,
):
    # TODO: Add templates from override
    # templates = jinja2.Environment(loader=jinja2.FileSystemLoader("templates/"))
    # print(templates.list_templates())
    # template = templates.get_template("index.html")
    index_template = importlib.resources.read_text(templates, "posts-list.html")

    context = {
        "posts": single_posts_chunk,
        "config": blog_config.plugin_config,
        "translation": blog_config.translation,
    }
    template = jinja2.Environment(loader=jinja2.BaseLoader()).from_string(index_template)

    page = frontmatter.Post(content=template.render(context))
    page["title"] = page_title

    with open(file_path, mode="wb") as teasers_index:
        frontmatter.dump(page, teasers_index)
