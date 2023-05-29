import urllib.parse

import pymdownx.slugs


def slugify(text: str) -> str:
    text = urllib.parse.unquote(text)
    text = pymdownx.slugs.slugify(case="lower", normalize="NFD")(text=text, sep="-")
    text = str(text).encode("ASCII", "ignore").decode("utf-8")
    return text
