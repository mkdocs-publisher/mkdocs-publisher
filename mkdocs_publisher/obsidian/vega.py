# MIT License
#
# Copyright (c) 2023 Maciej 'maQ' Kusz <maciej.kusz@gmail.com>
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

import json
import logging
import re
from typing import Optional

import jinja2

from mkdocs_publisher.obsidian.config import _ObsidianVegaConfig

log = logging.getLogger("mkdocs.plugins.publisher.obsidian.vega")


VEGA_BLOCK_START = re.compile(r"^( *)```(vega-lite|vega)")
VEGA_BLOCK_STOP = re.compile(r"^( *)```")
VEGA_CHART_TEMPLATE = """
<div id="vega-chart-{{ vega_chart_id }}"></div>
<script type="text/javascript">
  var vegaChart{{ vega_chart_id }} = {{ vega_chart }};
  vegaEmbed('#vega-chart-{{ vega_chart_id }}', vegaChart{{ vega_chart_id }})
  .then(result => console.log(result))
  .catch(console.warn);
</script>
"""


class VegaCharts:
    def __init__(self, vega_config: _ObsidianVegaConfig):
        self._vega_config: _ObsidianVegaConfig = vega_config
        self._vega_schema_mapping: dict = {
            "vega": self._vega_config.vega_schema,
            "vega-lite": self._vega_config.vega_lite_schema,
        }
        self._vega_chart_id: int = 0
        self._vega_found: bool = False

    @property
    def is_vega(self) -> bool:
        return self._vega_found

    def generate_charts(self, markdown: str) -> str:
        in_vega_block: bool = False
        vega_block_lines: list = []
        vega_schema: Optional[str] = None
        markdown_lines = []

        for line in markdown.split("\n"):
            vega_start_match = re.match(VEGA_BLOCK_START, line)
            if not in_vega_block and vega_start_match:
                in_vega_block = True
                vega_schema = self._vega_schema_mapping[vega_start_match.group(2)]
            elif in_vega_block:
                vega_stop_match = re.match(VEGA_BLOCK_STOP, line)
                if vega_stop_match:

                    # Create chart data as JSON
                    vega_chart_json = json.loads("\n".join(vega_block_lines))
                    if "$schema" not in vega_chart_json:
                        vega_chart_json["$schema"] = vega_schema

                    # Render chart
                    self._vega_chart_id += 1
                    vega_chart_context = {
                        "vega_chart_id": self._vega_chart_id,
                        "vega_chart": json.dumps(vega_chart_json),
                    }
                    vega_chart_template = jinja2.Environment(
                        loader=jinja2.BaseLoader()
                    ).from_string(VEGA_CHART_TEMPLATE)

                    vega_chart = vega_chart_template.render(vega_chart_context)

                    for vega_chart_line in vega_chart.split("\n"):
                        markdown_lines.append(vega_chart_line)

                    # Mark that vega is in that page
                    self._vega_found = True

                    # Restore default values
                    in_vega_block = False
                    vega_block_lines = []
                    vega_schema = None
                else:
                    vega_block_lines.append(line)
            else:
                markdown_lines.append(line)

        return "\n".join(line for line in markdown_lines)
