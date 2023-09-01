import logging

from mkdocs.config import config_options as option
from mkdocs.config.base import Config


class _DebuggerConsoleConfig(Config):
    enabled = option.Type(bool, default=True)
    # noinspection PyUnresolvedReferences,PyProtectedMember
    log_level = option.Choice(choices=logging._nameToLevel.keys(), default="INFO")
    show_code_link = option.Type(bool, default=False)
    show_logger_name = option.Type(bool, default=True)
    show_entry_time = option.Type(bool, default=True)
    entry_time_format = option.Type(str, default="%H:%M:%S.%f")
    filter_logger_names = option.Type(list, default=[])


class _DebuggerFileConfig(Config):
    enabled = option.Type(bool, default=True)
    # noinspection PyUnresolvedReferences,PyProtectedMember
    log_level = option.Choice(choices=logging._nameToLevel.keys(), default="DEBUG")
    log_format = option.Type(
        str, default="[%(created).14s][%(levelname)-5.5s][%(project_path)s:%(lineno)d] %(message)s"
    )
    remove_old_files = option.Type(bool, default=True)
    filter_logger_names = option.Type(list, default=[])


class _DebuggerZipConfig(Config):
    enabled = option.Type(bool, default=True)
    remove_old_files = option.Type(bool, default=True)
    add_pip_freeze = option.Type(bool, default=True)


class DebuggerConfig(Config):
    console_log: _DebuggerConsoleConfig = option.SubConfig(_DebuggerConsoleConfig)  # type: ignore
    file_log: _DebuggerFileConfig = option.SubConfig(_DebuggerFileConfig)  # type: ignore
    zip_log: _DebuggerZipConfig = option.SubConfig(_DebuggerZipConfig)  # type: ignore
