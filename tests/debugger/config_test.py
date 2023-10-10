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
#
# import logging
# from pathlib import Path
#
# import pytest
# from mkdocs.config import Config
# from mkdocs.config.defaults import MkDocsConfig
# from mkdocs_publisher.debugger import plugin
# import yaml
# import tempfile
# from pytest import LogCaptureFixture
#
# log = logging.getLogger("mkdocs")
# log.addHandler(logging.StreamHandler())
#
#
# def test_any(caplog: LogCaptureFixture):
#     config = MkDocsConfig()
#     yaml_config = {"plugins": [{"pub-debugger": {"console_log": {"enabled": True}}}]}
#
#     with tempfile.NamedTemporaryFile(mode="w+") as config_file:
#         yaml.safe_dump(data=yaml_config, stream=config_file)
#         config_file.seek(0)
#         config.load_file(config_file=config_file)
#     print(config)
#
#     # with caplog.
#     t = plugin.DebuggerPlugin()
#     t.load_config(options=yaml_config)
#     print(t.config)
