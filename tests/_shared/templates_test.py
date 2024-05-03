# MIT License
#
# Copyright (c) 2023-2024 Maciej 'maQ' Kusz <maciej.kusz@gmail.com>
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

import re

from pytest_check import check_functions as check

from mkdocs_publisher._shared import templates

HTML_COMMENT_RE = re.compile(r"<!--(.*)-->", re.DOTALL)
TEMPLATE_FILE = "backlinks.html"


def test_templates_render():
    """Test if content of the template file is read correctly"""

    exp_template = (
        '<p class="obsidian_backlink_title">Test:</p>'
        '<div class="obsidian_backlink" markdown=1></div>'
    )
    render = templates.render(tpl_file=TEMPLATE_FILE, context={"title": "Test"})
    render = re.sub(HTML_COMMENT_RE, "", render).replace("\n", "")
    check.equal(exp_template, render)
