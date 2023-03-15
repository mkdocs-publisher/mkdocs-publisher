import logging
import subprocess
from hashlib import md5
from pathlib import Path
from typing import List
from typing import Optional
from typing import cast
from uuid import uuid4

from mkdocs import utils
from mkdocs.config import Config
from mkdocs.plugins import BasePlugin

log = logging.getLogger("mkdocs.plugins.publisher.common")


def get_plugin_config(
    plugin: BasePlugin, config_file_path: str, yaml_config_key: str
) -> Optional[Config]:
    options = {}
    yaml_config_file = cast(dict, utils.yaml_load(open(config_file_path, "rb")))
    plugin_config_found = False
    for plugin_config in cast(list, yaml_config_file.get("plugins")):
        if isinstance(plugin_config, dict) and list(plugin_config.keys())[0] == yaml_config_key:
            plugin_config_found = True
            options = list(plugin_config.values())[0]
        elif isinstance(plugin_config, str) and plugin_config == yaml_config_key:
            plugin_config_found = True
    plugin.load_config(options=options, config_file_path=config_file_path)

    return plugin.config if plugin_config_found else None


def run_subprocess(cmd) -> int:
    cmd = [arg for arg in cmd if arg is not None]
    log.debug(f"Run cmd: {' '.join(cmd)}")
    call_output = subprocess.run(cmd)
    return call_output.returncode


def remove_dir(directory: Path):
    for file in directory.iterdir():
        if file.is_dir():
            remove_dir(directory=file)
            file.rmdir()
        else:
            file.unlink(missing_ok=True)


def calculate_file_hash(file: Path, block_size: int = 8192) -> str:
    with open(file, "rb") as binary_file:
        hash = md5()
        while chunk := binary_file.read(block_size):
            hash.update(chunk)
        return hash.hexdigest()


def list_files(
    directory: Path, extensions: Optional[List[str]] = None, relative_to: Optional[Path] = None
) -> List[Path]:
    files_list: List[Path] = []
    for file in directory.iterdir():
        if file.is_dir():
            files_list.extend(
                list_files(directory=file, extensions=extensions, relative_to=relative_to)
            )
        elif str(file.suffix).lower() in extensions or extensions is None:  # type: ignore
            files_list.append(file if relative_to is None else file.relative_to(relative_to))
    return files_list


def get_hashed_file_name(file: Path) -> Path:
    return Path(file.with_name(f"{str(uuid4()).replace('-', '')}{str(file.suffix).lower()}").name)
