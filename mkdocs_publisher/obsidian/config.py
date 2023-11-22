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

from mkdocs.config import config_options as option
from mkdocs.config.base import Config


class _ObsidianBacklinksConfig(Config):
    enabled = option.Type(bool, default=True)


class _ObsidianCalloutsConfig(Config):
    enabled = option.Type(bool, default=True)
    indentation = option.Choice(["tabs", "spaces"], default="spaces")


class _ObsidianCommentsConfig(Config):
    enabled = option.Type(bool, default=True)
    inject_as_html = option.Type(bool, default=False)


class _ObsidianVegaConfig(Config):
    enabled = option.Type(bool, default=True)
    vega_schema = option.Type(str, default="https://vega.github.io/schema/vega/v5.json")
    vega_lite_schema = option.Type(str, default="https://vega.github.io/schema/vega-lite/v5.json")


class _ObsidianLinksConfig(Config):
    wikilinks_enabled = option.Type(bool, default=True)
    img_lazy_loading = option.Type(bool, default=True)


class ObsidianPluginConfig(Config):
    # TODO: read those values from Obsidian config files
    obsidian_dir = option.Type(str, default=".obsidian")
    templates_dir = option.Type(str, default="_templates")
    attachments_dir = option.Type(str, default="_attachments")

    backlinks: _ObsidianBacklinksConfig = option.SubConfig(_ObsidianBacklinksConfig)  # type: ignore
    callouts: _ObsidianCalloutsConfig = option.SubConfig(_ObsidianCalloutsConfig)  # type: ignore
    comments: _ObsidianCommentsConfig = option.SubConfig(_ObsidianCommentsConfig)  # type: ignore
    vega: _ObsidianVegaConfig = option.SubConfig(_ObsidianVegaConfig)  # type: ignore
    links: _ObsidianLinksConfig = option.SubConfig(_ObsidianLinksConfig)  # type: ignore
