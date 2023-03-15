import logging
from collections import OrderedDict
from dataclasses import fields
from datetime import datetime
from pathlib import Path

import frontmatter

from blog.structures import BlogConfig
from blog.structures import BlogPost

log = logging.getLogger("mkdocs.plugins.publisher.blog")

REQUIRED_META_KEYS = ["title", "date", "slug", "tags", "categories", "description"]


def parse_markdown_files(
    blog_config: BlogConfig,
    config_nav: OrderedDict,
):
    """Parse all markdown files and extract blog posts from `blog_dir` (default: 'posts').
    BlogPost object is created and filled with content and metadata of the post.
    """
    log.info(f"Parsing blog posts from '{blog_config.blog_dir}' directory")
    for file_path in blog_config.docs_dir.glob("**/*"):
        if blog_config.auto_nav_config is not None:
            if file_path.parts[-1] == blog_config.auto_nav_config.meta_file_name:
                continue
        file_path = Path(file_path)
        path = Path(file_path).relative_to(blog_config.docs_dir)
        if (
            file_path.is_file()
            and path.is_relative_to(blog_config.blog_dir)
            and path.suffix == ".md"
        ):
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
