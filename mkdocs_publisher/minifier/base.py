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

import logging
from dataclasses import asdict
from dataclasses import dataclass
from dataclasses import field
from pathlib import Path
from threading import Semaphore
from threading import Thread
from typing import Optional

from mkdocs.config.defaults import MkDocsConfig

# noinspection PyProtectedMember
from mkdocs_publisher._shared import file_utils
from mkdocs_publisher.minifier.config import MinifierConfig
from mkdocs_publisher.minifier.config import _MinifierCommonConfig

log = logging.getLogger("mkdocs.plugins.publisher.minifier.base")


@dataclass
class CachedFile:
    original_file_hash: str = field(default="")
    original_file_path: Path = field(default_factory=lambda: Path(""))
    cached_file_name: Path = field(default_factory=lambda: Path(""))

    def __init__(
        self,
        original_file_hash: str = "",
        original_file_path: str = "",
        cached_file_name: str = "",
    ):
        self.original_file_hash = original_file_hash
        self.original_file_path = Path(original_file_path)
        self.cached_file_name = Path(cached_file_name)

    def based_on(self, file: Path, directory: Path):
        self.original_file_path = file
        self.original_file_hash = file_utils.calculate_file_hash(file=directory / file)
        self.cached_file_name = file_utils.get_hashed_file_name(file=file)

    @property
    def as_dict(self) -> dict:
        return asdict(self)


class BaseMinifier:
    def __init__(
        self,
        plugin_config: MinifierConfig,
        mkdocs_config: MkDocsConfig,
        cached_files: dict[str, CachedFile],
    ):
        self._plugin_config: MinifierConfig = plugin_config
        self._mkdocs_config: MkDocsConfig = mkdocs_config
        self._minify_options: Optional[_MinifierCommonConfig] = None
        self._cached_files: dict[str, CachedFile] = cached_files
        self._cache_enabled: bool = self._plugin_config.cache_enabled
        self._exclude: list = self._plugin_config.exclude[:]

    def minifier(self, cached_file: CachedFile) -> Optional[CachedFile]:
        raise NotImplementedError

    def __call__(self):
        minifier_name = self.__class__.__name__.replace("Minifier", "").upper()
        self._cache_enabled = self._minify_options.cache_enabled if self._cache_enabled else False
        self._exclude.extend(self._minify_options.exclude)

        log.info(
            f"Minifying {minifier_name} files ({'with' if self._cache_enabled else 'no'} cache)"
        )
        log.info(f"Excluded {minifier_name} files patterns: {self._exclude}")

        semaphore = Semaphore(self._plugin_config.threads)
        threads = []

        for file in file_utils.list_files(
            directory=Path(self._mkdocs_config.site_dir),
            extensions=self._minify_options.extensions,
            exclude=self._exclude,
        ):
            log.debug(f"Minifying: {file}")
            semaphore.acquire()
            thread = Thread(
                target=self._minify_with_cache,
                kwargs={
                    "file": file,
                    "cache_enabled": self._cache_enabled,
                    "semaphore": semaphore,
                },
            )
            thread.start()
            threads.append(thread)

        # Wait for all threads to be finished
        for thread in threads:
            thread.join()

    def _is_new_smaller(self, cached_file: CachedFile) -> Optional[CachedFile]:
        old_file = self._mkdocs_config.site_dir / cached_file.original_file_path
        new_file = self._plugin_config.cache_dir / cached_file.cached_file_name
        new_file_size = new_file.stat().st_size
        old_file_size = old_file.stat().st_size
        log.debug(
            f"Minified: '{old_file.relative_to(self._mkdocs_config.site_dir)}' "
            f"(size: {old_file_size} -> {new_file_size})"
        )
        log.debug(
            f"{old_file.relative_to(self._mkdocs_config.site_dir)} -> "
            f"{new_file.relative_to(self._plugin_config.cache_dir)} "
        )
        if new_file_size < old_file_size:
            return cached_file

        log.debug(
            f"Minified file larger than original: "
            f"{cached_file.original_file_path} (removing cached file)"
        )
        new_file.unlink()
        return None

    def _copy_cached_file(self, cached_file: CachedFile):
        original_file = self._mkdocs_config.site_dir / cached_file.original_file_path
        cache_file = self._plugin_config.cache_dir / cached_file.cached_file_name
        try:
            original_file.write_bytes(cache_file.read_bytes())
        except FileNotFoundError as e:
            log.warning(e)

    def _minify_with_cache(self, file: Path, cache_enabled: bool, semaphore: Semaphore):
        recreate_file = False
        if cache_enabled and str(file) in self._cached_files:
            log.debug(f"{file} is in cache")
            file_hash = file_utils.calculate_file_hash(file=(self._mkdocs_config.site_dir / file))
            cached_file = self._cached_files[str(file)]
            if cached_file.original_file_hash == file_hash:
                log.debug(f"{file} hash is equal to one in cache (file: {file_hash})")
                cached_file_name = self._plugin_config.cache_dir / cached_file.cached_file_name
                if cached_file_name.exists():
                    self._copy_cached_file(cached_file=cached_file)
                else:
                    recreate_file = True
            else:
                log.debug(
                    f"{file} hash is not equal to one in cache "
                    f"(file: {file_hash} | cache: {cached_file.original_file_hash})"
                )
                recreate_file = True
        else:
            log.debug(f"{file} is not in cache (rebuilding")

            cached_file = CachedFile()
            cached_file.based_on(file=file, directory=Path(self._mkdocs_config.site_dir))
            recreate_file = True

        if recreate_file:
            log.debug(f"Minifying file: {file} (putting into cache)")
            cached_file = self.minifier(cached_file=cached_file)
            if cached_file:
                cached_file = self._is_new_smaller(cached_file=cached_file)
            if cached_file:
                self._cached_files[str(cached_file.original_file_path)] = cached_file
                self._copy_cached_file(cached_file=cached_file)
        else:
            log.debug(f"{file} is already minified (retrieving from cache)")
        semaphore.release()
