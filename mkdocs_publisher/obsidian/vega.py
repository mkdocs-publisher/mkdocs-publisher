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

                    # Restore default values
                    in_vega_block = False
                    vega_block_lines = []
                    vega_schema = None
                else:
                    vega_block_lines.append(line)
            else:
                markdown_lines.append(line)

        return "\n".join(line for line in markdown_lines)
