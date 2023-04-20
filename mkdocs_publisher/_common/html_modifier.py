from typing import List

from bs4 import BeautifulSoup


class HTMLModifier:
    def __init__(self, markup: str):
        self._soup = BeautifulSoup(markup=markup, features="html.parser")

    def __repr__(self):
        return self._soup.prettify()

    def add_head_script(self, src: str):
        """Add script to the head section"""
        self._soup.head.append(self._soup.new_tag(name="script", attrs={"src": src}))  # type: ignore

    def add_meta_property(self, name: str, value: str):
        """Add property to the head section"""
        self._soup.head.append(  # type: ignore
            self._soup.new_tag(name="meta", attrs={"property": name, "content": value})
        )

    def remove_meta_properties(self, properties: List[str]):
        """Remove meta tags with given properties from head section"""
        for prop in properties:
            head_property = self._soup.head.find(name="meta", attr={"property": prop})  # type: ignore
            if head_property is not None:
                head_property.extract()
