import click

from src.cli import post


@click.group
def app():
    pass


app.add_command(cmd=post.group, name="post")


if __name__ == "__main__":
    app()
