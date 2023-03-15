import click

# from src.cli import post


@click.group
def app():
    """Publisher plugin for MkDocs (by Maciej 'maQ' Kusz)
    More information can be fount at: https://github.com/mkusz/mkdocs-publisher
    """
    pass


# app.add_command(cmd=post.group, name="post")


if __name__ == "__main__":
    app()
