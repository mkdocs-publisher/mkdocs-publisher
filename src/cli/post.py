from pathlib import Path

import click
import frontmatter

# from src.cli._utils import blog_in_cfg
# from src.cli._utils import mkdocs_cfg


@click.group
def group():
    pass


@group.command
def create():
    post = frontmatter.Post(content="")
    post["date"] = "2022-01-02 19:22:23"
    post["tags"] = "some, any, none"
    post["category"] = "none"

    post_file_path = Path.cwd() / "docs/posts/temp.md"
    with open(post_file_path, "wb") as post_file:
        frontmatter.dump(post, fd=post_file)


# @group.command
# def temp(mkdocs_cfg=mkdocs_cfg(), blogger_cfg=blogger_cfg()):
#     print(blogger_cfg.images_dir)
