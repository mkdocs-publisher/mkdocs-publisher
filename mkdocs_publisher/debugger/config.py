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

from mkdocs.config import config_options as option
from mkdocs.config.base import Config

# noinspection PyUnresolvedReferences,PyProtectedMember
_ALL_LOG_LEVEL_NAMES = [k for key in logging._nameToLevel for k in [key, key.lower()]]  # noqa: SLF001


class _DebuggerConsoleConfig(Config):
    enabled = option.Type(bool, default=True)
    log_level = option.Choice(choices=_ALL_LOG_LEVEL_NAMES, default="INFO")
    show_code_link = option.Type(bool, default=False)
    show_logger_name = option.Type(bool, default=True)
    show_entry_time = option.Type(bool, default=True)
    show_deprecation_warnings = option.Type(bool, default=False)
    time_format = option.Type(str, default="%H:%M:%S.%f")
    filter_logger_names = option.Type(list, default=[])


class _DebuggerFileConfig(Config):
    enabled = option.Type(bool, default=True)
    log_level = option.Choice(choices=_ALL_LOG_LEVEL_NAMES, default="DEBUG")
    log_format = option.Type(
        str,
        default="[%(asctime)s.%(msecs)03d][%(levelname)-5.5s][%(project_path)s:%(lineno)d] %(message)s",
    )
    time_format = option.Type(str, default="%H:%M:%S")
    remove_old_files = option.Type(bool, default=True)
    filter_logger_names = option.Type(list, default=[])


class _DebuggerZipConfig(Config):
    enabled = option.Type(bool, default=True)
    remove_old_files = option.Type(bool, default=True)
    add_pip_freeze = option.Type(bool, default=True)


class DebuggerPluginConfig(Config):
    console_log: _DebuggerConsoleConfig = option.SubConfig(_DebuggerConsoleConfig)  # type: ignore[reportAssignmentType]
    file_log: _DebuggerFileConfig = option.SubConfig(_DebuggerFileConfig)  # type: ignore[reportAssignmentType]
    zip_log: _DebuggerZipConfig = option.SubConfig(_DebuggerZipConfig)  # type: ignore[reportAssignmentType]
