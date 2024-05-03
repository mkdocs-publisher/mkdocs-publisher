# MIT License
#
# Copyright (c) 2023-2024 Maciej 'maQ' Kusz <maciej.kusz@gmail.com>
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
from datetime import datetime
from pathlib import Path
from typing import cast

import yaml
from mkdocs.structure.files import File
from mkdocs.structure.files import Files

from mkdocs_publisher._shared import templates
from mkdocs_publisher._shared.urls import slugify
from mkdocs_publisher.blog.structures import BlogConfig

log = logging.getLogger("mkdocs.plugins.publisher.blog.creators")


def create_blog_files(
    blog_config: BlogConfig,
    files: Files,
):
    for temp_file in blog_config.temp_files.values():
        try:
            file = File(
                path=str(Path(temp_file).relative_to(blog_config.temp_dir)),
                src_dir=str(blog_config.temp_dir),
                dest_dir=str(blog_config.site_dir),
                use_directory_urls=blog_config.mkdocs_config.use_directory_urls,
            )
            files.append(file)
        except ValueError:
            pass


def create_blog_post_pages(
    start_page: bool,
    blog_config: BlogConfig,
    config_nav: OrderedDict,
) -> None:
    """Create blog posts index files."""

    log.info("Creating blog posts index files")
    posts_chunks: dict[str, list] = {}
    archive_chunks: dict[str, list] = {}
    categories_chunks: dict[str, list] = {}
    tags_chunks: dict[str, list] = {}

    # Build post index pages
    for index, date in enumerate(sorted(blog_config.blog_posts, reverse=True)):
        index = (
            "index"
            if start_page and index < blog_config.plugin_config.posts_per_page
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

        categories = cast(str, blog_config.blog_posts[date].categories)
        for category in categories:
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
    config_nav[blog_config.translation.blog_navigation_name] = []

    for key, single_posts_chunk in posts_chunks.items():
        file_name = f"{key}.md"
        file_path = blog_config.temp_dir / file_name

        _render_and_write_page(
            single_posts_chunk=single_posts_chunk,
            file_path=file_path,
            blog_config=blog_config,
            page_title=blog_config.translation.blog_page_title,
        )

        blog_config.temp_files[f"{blog_config.translation.blog_navigation_name}/{key}"] = file_path
        log.debug(f"Creating blog post chunk file: {file_path}")

        config_nav[blog_config.translation.blog_navigation_name].append({key: file_name})

    config_nav[blog_config.translation.blog_navigation_name].append(
        {
            blog_config.translation.archive_navigation_name: _create_pages(
                blog_config=blog_config,
                posts_chunks=archive_chunks,
                sub_dir=Path(blog_config.plugin_config.archive_subdir),
                page_title=blog_config.translation.archive_page_title,
            )
        }
    )

    config_nav[blog_config.translation.blog_navigation_name].append(
        {
            blog_config.translation.categories_navigation_name: _create_pages(
                blog_config=blog_config,
                posts_chunks=categories_chunks,
                sub_dir=Path(blog_config.plugin_config.categories_subdir),
                page_title=blog_config.translation.categories_page_title,
            )
        }
    )

    config_nav[blog_config.translation.blog_navigation_name].append(
        {
            blog_config.translation.tags_navigation_name: _create_pages(
                blog_config=blog_config,
                posts_chunks=tags_chunks,
                sub_dir=Path(blog_config.plugin_config.tags_subdir),
                page_title=blog_config.translation.tags_page_title,
            )
        }
    )


def _create_pages(
    blog_config: BlogConfig,
    posts_chunks: dict[str, list],
    sub_dir: Path,
    page_title: str,
) -> list[dict[str, str]]:
    config_nav = []

    blog_temp_dir = blog_config.temp_dir / blog_config.plugin_config.blog_dir
    blog_temp_dir.mkdir(exist_ok=True)

    pages_dir = blog_temp_dir / sub_dir
    pages_dir.mkdir(exist_ok=True)

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

        config_nav.append({key: f"{blog_config.plugin_config.blog_dir}/{sub_dir}/{file_name}"})
    return config_nav


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

    post_context = {
        "posts": single_posts_chunk,
        "site_url": str(blog_config.mkdocs_config.site_url),
        "config": blog_config.plugin_config,
        "translation": blog_config.translation,
    }
    markdown = templates.render(tpl_file="posts-list.html", context=post_context)

    # TODO: when using pub-meta key name should be taken from plugin config
    page_meta = {"title": page_title}
    # TODO: consider moving slugify configuration to mkdocs.yaml
    if file_path.name.startswith("index-0"):
        slug = blog_config.plugin_config.slug
    elif file_path.name.startswith("index"):
        slug = f"{blog_config.plugin_config.slug}/{file_path.stem.split('-')[-1]}"
    else:
        slug = slugify(text=page_title.split("-")[-1].strip())
    page_meta["slug"] = slug
    page_meta["publish"] = "true"
    if not blog_config.plugin_config.searchable_non_posts:
        page_meta["search"] = {"exclude": True}  # type: ignore

    with open(file_path, mode="w") as teasers_index:
        teasers_index.write(f"---\n{yaml.dump(page_meta)}\n---\n\n{markdown}")
