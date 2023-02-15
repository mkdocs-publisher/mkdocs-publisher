import logging
from collections import OrderedDict
from dataclasses import fields
from datetime import datetime
from pathlib import Path
from typing import Dict

import frontmatter

from src.plugin.structures import BlogPost

log = logging.getLogger("mkdocs.plugins.blog-in")


def parse_markdown_files(
    blog_posts: Dict[datetime, BlogPost],
    config_nav: OrderedDict,
    docs_dir: Path,
    posts_dir: Path,
):
    """Parse all markdown files and extract blog posts from `posts_dir` (default: 'posts').
    BlogPost object is created and filled with content and metadata of the post.
    """
    log.info(f"Parsing blog posts from '{posts_dir}' directory")
    for file_path in docs_dir.glob("**/*"):
        file_path = Path(file_path)
        path = Path(file_path).relative_to(docs_dir)
        if file_path.is_file() and path.suffix == ".md":
            parents = list(path.parents)[:-1]
            with open(file_path) as markdown_file:
                post = frontmatter.load(markdown_file)
                if not parents:
                    for line in post.content.split("\n"):
                        if line.startswith("# "):
                            config_nav[line[2:]] = str(path)
                elif str(parents[0]) == str(posts_dir):
                    post_meta = dict(post)

                    # Convert tags format
                    if "," in post_meta["tags"]:
                        post_meta["tags"] = [t.strip() for t in post_meta["tags"].split(",")]
                    elif isinstance(post_meta["tags"], str):
                        post_meta["tags"] = [post_meta["tags"]]

                    # Create a new blog post
                    blog_post_keys = [f.name for f in fields(BlogPost)]
                    post_data = {k: v for k, v in post_meta.items() if k in blog_post_keys}
                    post_data["content"] = post.content
                    post_data["path"] = str(path)
                    if "slug" in post_meta and post_meta["slug"].strip() != "":
                        post_data["slug"] = f"{posts_dir}/{post_meta['slug']}"
                    blog_post: BlogPost = BlogPost(**post_data)

                    # Add new post to blog posts collection
                    blog_posts[blog_post.date] = blog_post
                    log.debug(f"New blog posts: {blog_post.title}")


def create_blog_post_teaser(blog_posts: Dict[datetime, BlogPost], teaser_marker: str):
    """Extracting beginning of a blog content as a teaser. End of a teaser is determined by
    'teaser_marker' config value (default: '<!-- more -->'). When not found entire blog post
    is considered a teaser and link to full blog posts is not displayed, but whole blog post
    is still rendered, so it can be navigated to from other blog post using next/previous page
    arrows at the bottom of the page.
    """
    for date in sorted(blog_posts, reverse=True):
        content = []
        for line in blog_posts[date].content.split("\n"):  # type: ignore
            if line == teaser_marker:
                blog_posts[date].is_teaser = True
                blog_posts[date].teaser = "\n".join(c for c in content)
            content.append(line)
        if not blog_posts[date].is_teaser:
            blog_posts[date].teaser = "\n".join(c for c in content)
        log.debug(f"Post: '{blog_posts[date].title}' is teaser: {blog_posts[date].is_teaser}")
