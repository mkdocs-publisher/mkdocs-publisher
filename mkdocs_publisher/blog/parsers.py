import logging
import re
from collections import OrderedDict
from dataclasses import fields
from datetime import datetime
from pathlib import Path

import frontmatter

from mkdocs_publisher.blog.structures import BlogConfig
from mkdocs_publisher.blog.structures import BlogPost

log = logging.getLogger("mkdocs.plugins.publisher.blog")

REQUIRED_META_KEYS = ["title", "date", "slug", "tags", "categories", "description"]


def count_words(content):
    """Count words in markdown content.

    This code is based on: https://github.com/gandreadis/markdown-word-count
    """
    content = re.sub(r"<!--(.*?)-->", "", content, flags=re.MULTILINE)  # Comments
    content = content.replace("\t", "    ")  # Tabs to spaces
    content = re.sub(r"[ ]{2,}", "    ", content)  # More than 1 space to 4 spaces
    content = re.sub(r"^\[[^]]*][^(].*", "", content, flags=re.MULTILINE)  # Footnotes
    content = re.sub(
        r"^( {4,}[^-*]).*", "", content, flags=re.MULTILINE
    )  # Indented blocks of code
    content = re.sub(r"{#.*}", "", content)  # Custom header IDs
    content = content.replace("\n", " ")  # Replace newlines with spaces for uniform handling
    content = re.sub(r"!\[[^]]*]\([^)]*\)", "", content)  # Remove images
    content = re.sub(r"</?[^>]*>", "", content)  # Remove HTML tags
    content = re.sub(r"[#*`~\-–^=<>+|/:]", "", content)  # Remove special characters
    content = re.sub(r"\[[0-9]*]", "", content)  # Remove footnote references
    content = re.sub(r"[0-9#]*\.", "", content)  # Remove enumerations

    return len(content.split())


# from mkdocs.utils import meta as meta_parser
# with file.open(encoding="utf-8-sig", errors="strict") as md_file:
#     markdown, meta = meta_parser.get_data(md_file.read())


def parse_markdown_files(
    blog_config: BlogConfig,
    config_nav: OrderedDict,
    on_serve: bool = False,
):
    """Parse all markdown files and extract blog posts from `blog_dir` (default: 'posts').
    BlogPost object is created and filled with content and metadata of the post.
    """
    log.info(f"Parsing blog posts from '{blog_config.blog_dir}' directory")
    for file_path in blog_config.docs_dir.glob("**/*.md"):
        if blog_config.meta_config is not None:
            if file_path.parts[-1] == blog_config.meta_config.meta_file_name:
                continue
        file_path = Path(file_path)
        path = Path(file_path).relative_to(blog_config.docs_dir)
        if path.is_relative_to(blog_config.blog_dir):
            parents = list(path.parents)[:-1]
            with open(file_path) as markdown_file:
                post: frontmatter.Post = frontmatter.load(markdown_file)
                if not parents:
                    for line in post.content.split("\n"):
                        if line.startswith("# "):
                            config_nav[line[2:]] = str(path)
                elif str(parents[0]) == str(blog_config.blog_dir):
                    post_meta = dict(post)

                    if "status" not in post_meta:
                        log.info(
                            f"File: {file_path} - missing 1 required positional argument: "
                            f"'status' (setting to default: draft)"
                        )
                        post_meta["status"] = "draft"

                    # Skip non published
                    if not on_serve and post_meta["status"] != "published":
                        # TODO: make it configurable
                        continue

                    # Convert tags format
                    if "tags" in post_meta and post_meta["tags"] is not None:
                        if "," in post_meta["tags"]:
                            post_meta["tags"] = [t.strip() for t in post_meta["tags"].split(",")]
                        elif isinstance(post_meta["tags"], str):
                            post_meta["tags"] = [post_meta["tags"]]
                    else:
                        post_meta["tags"] = ["undefined"]  # TODO: move this value to config

                    # Convert categories format
                    if "categories" in post_meta and post_meta["categories"] is not None:
                        if "," in post_meta["categories"]:
                            post_meta["categories"] = [
                                t.strip() for t in post_meta["categories"].split(",")
                            ]
                        elif isinstance(post_meta["categories"], str):
                            post_meta["categories"] = [post_meta["categories"]]
                    else:
                        post_meta["categories"] = ["undefined"]  # TODO: move this value to config

                    # Setup date to current one, when missing
                    if "date" in post_meta and post_meta["date"] is None:
                        post_meta["date"] = datetime.utcnow()

                    # Create a new blog post
                    blog_post_keys = [f.name for f in fields(BlogPost)]
                    post_data = {k: v for k, v in post_meta.items() if k in blog_post_keys}
                    post_data["content"] = post.content
                    post_data["path"] = str(path)
                    if "slug" in post_meta and post_meta["slug"].strip() != "":
                        post_data["slug"] = post_meta["slug"]
                    try:
                        blog_post: BlogPost = BlogPost(**post_data)

                        # Add new post to blog posts collection
                        blog_config.blog_posts[blog_post.date] = blog_post
                        log.debug(f"New blog posts: {blog_post.title}")
                    except TypeError as e:
                        msg = str(e).replace("__init__()", f"File: {file_path} -")
                        log.warning(msg)

                    # TODO: add reading time
                    # print(f"{file_path} - {count_words(post.content) / 265 * 60}")


def create_blog_post_teaser(blog_config: BlogConfig):
    """Extracting beginning of a blog content as a teaser. End of a teaser is determined by
    'teaser_marker' config value (default: '<!-- more -->'). When not found entire blog post
    is considered a teaser and link to full blog posts is not displayed, but whole blog post
    is still rendered, so it can be navigated to from other blog post using next/previous page
    arrows at the bottom of the page.
    """
    for date in sorted(blog_config.blog_posts, reverse=True):
        content = []
        for line in blog_config.blog_posts[date].content.split("\n"):  # type: ignore
            if line == blog_config.plugin_config.teaser_marker:
                blog_config.blog_posts[date].is_teaser = True
                blog_config.blog_posts[date].teaser = "\n".join(c for c in content)
            content.append(line)
        if not blog_config.blog_posts[date].is_teaser:
            blog_config.blog_posts[date].teaser = "\n".join(c for c in content)
        log.debug(
            f"Post: '{blog_config.blog_posts[date].title}' "
            f"is teaser: {blog_config.blog_posts[date].is_teaser}"
        )
