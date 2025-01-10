# MIT License
#
# Copyright (c) 2023-2025 Maciej 'maQ' Kusz <maciej.kusz@gmail.com>
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

from bs4 import BeautifulSoup

log = logging.getLogger("mkdocs.publisher._shared.html_modifiers")


class HTMLModifier:
    """HTML modifications"""

    def __init__(self, markup: str):
        self._soup = BeautifulSoup(markup=markup, features="html.parser")

    def __repr__(self):
        return str(self._soup)

    def add_head_script(self, src: str):
        """Add script to the head section"""
        self._soup.head.append(  # type: ignore
            self._soup.new_tag(name="script", attrs={"src": src})
        )

    def add_meta_property(self, name: str, value: str):
        """Add property to the head section"""
        self._soup.head.append(  # type: ignore
            self._soup.new_tag(name="meta", attrs={"property": name, "content": value})
        )

    def remove_meta_properties(self, properties: list[str]):
        """Remove meta tags with given properties from head section"""
        for prop in properties:
            head_property = self._soup.head.find(name="meta", attr={"property": prop})  # type: ignore
            if head_property is not None:
                head_property.extract()
