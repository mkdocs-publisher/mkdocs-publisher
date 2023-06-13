import urllib.parse

import pymdownx.slugs


def slugify(text: str) -> str:
    """Text slugify function that produces the same slug as MkDocs one"""

    text = urllib.parse.unquote(text)
    text = pymdownx.slugs.slugify(case="lower", normalize="NFD")(text=text, sep="-")
    return str(text).encode("ASCII", "ignore").decode("utf-8")
