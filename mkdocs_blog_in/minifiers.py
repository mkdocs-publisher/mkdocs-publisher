import logging
from pathlib import Path
from sys import exit
from threading import Semaphore
from threading import Thread
from typing import List
from typing import Optional

import yaml

import mkdocs_blog_in.utils as utils
from mkdocs_blog_in.structures import BlogConfig
from mkdocs_blog_in.structures import CachedFile

log = logging.getLogger("mkdocs.plugins.blog-in")


def _svg_minifier(cached_file: CachedFile, blog_config: BlogConfig) -> Optional[CachedFile]:
    minify_svg_options = blog_config.plugin_config.minify.svg
    try:
        input_file = blog_config.site_dir / cached_file.original_file_path
        output_file = blog_config.cache_dir / cached_file.cached_file_name

        svgo_cmd = [
            minify_svg_options.svgo_path,
            "--multipass" if minify_svg_options.multipass else None,
            "--quiet",
            "--output",
            str(output_file),
            "--input",
            str(input_file),
        ]
        if utils.run_subprocess(cmd=svgo_cmd) != 0:
            output_file.unlink(missing_ok=True)
            return None

        is_new_smaller = utils.is_new_smaller(
            old_file=input_file, new_file=output_file, blog_config=blog_config
        )
        if is_new_smaller:
            return cached_file
        else:
            log.debug(
                f"Minified file larger than original: "
                f"{cached_file.original_file_path} (removing cached file)"
            )
            output_file.unlink()
    except FileNotFoundError as e:
        log.warning(e)

    return None


def _jpg_minifier(cached_file: CachedFile, blog_config: BlogConfig) -> Optional[CachedFile]:
    minify_jpg_options = blog_config.plugin_config.minify.jpg
    try:
        input_file = blog_config.site_dir / cached_file.original_file_path
        output_file = blog_config.cache_dir / cached_file.cached_file_name

        djpg_cmd = [
            minify_jpg_options.djpeg_path,
            "-targa",
            "-outfile",
            str(output_file.with_suffix(".tga")),
            str(input_file),
        ]
        if utils.run_subprocess(cmd=djpg_cmd) != 0:
            output_file.with_suffix(".tga").unlink(missing_ok=True)
            return None

        cjpg_cmd = [
            minify_jpg_options.cjpeg_path,
            "-targa",
            "-smooth" if int(minify_jpg_options.smooth) > 0 else None,
            minify_jpg_options.smooth if int(minify_jpg_options.smooth) > 0 else None,
            "-quality" if int(minify_jpg_options.quality) > 0 else None,
            minify_jpg_options.quality if int(minify_jpg_options.quality) > 0 else None,
            "-outfile",
            str(output_file.with_suffix(".jpg_")),
            str(output_file.with_suffix(".tga")),
        ]
        if utils.run_subprocess(cmd=cjpg_cmd) != 0:
            output_file.with_suffix(".jpg_").unlink(missing_ok=True)
            return None
        output_file.with_suffix(".tga").unlink(missing_ok=True)

        jpegtran_cmd = [
            minify_jpg_options.jpegtran_path,
            "-copy",
            minify_jpg_options.copy_meta,
            "-progressive" if minify_jpg_options.progressive else None,
            "-optimise" if minify_jpg_options.optimise else None,
            "-outfile",
            str(output_file),
            str(output_file.with_suffix(".jpg_")),
        ]
        if utils.run_subprocess(cmd=jpegtran_cmd) != 0:
            output_file.unlink(missing_ok=True)
            return None
        output_file.with_suffix(".jpg_").unlink(missing_ok=True)

        is_new_smaller = utils.is_new_smaller(
            old_file=input_file, new_file=output_file, blog_config=blog_config
        )
        if is_new_smaller:
            return cached_file
        else:
            log.debug(
                f"Minified file larger than original: "
                f"{cached_file.original_file_path} (removing cached file)"
            )
            output_file.unlink()
    except FileNotFoundError as e:
        log.warning(e)

    return None


def _png_minifier(cached_file: CachedFile, blog_config: BlogConfig) -> Optional[CachedFile]:
    minify_png_options = blog_config.plugin_config.minify.png
    try:
        input_file = blog_config.site_dir / cached_file.original_file_path
        output_file = blog_config.cache_dir / cached_file.cached_file_name

        if minify_png_options.pngquant_enabled:
            pngquant_cmd = [
                minify_png_options.pngquant_path,
                "--force",
                "--strip" if minify_png_options.strip else None,
                "--speed",
                minify_png_options.pngquant_speed,
                "--output",
                str(output_file),
                str(input_file),
            ]
            if utils.run_subprocess(cmd=pngquant_cmd) != 0:
                output_file.unlink(missing_ok=True)
                return None

        if minify_png_options.oxipng_enabled:
            oxipng_cmd = [
                minify_png_options.oxipng_path,
                "--quiet",
                "--force",
                "--strip" if minify_png_options.strip else None,
                "all" if minify_png_options.strip else None,
                "--zopfli" if minify_png_options.oxipng_max_compression else None,
                "--out" if not minify_png_options.pngquant_enabled else None,
                str(output_file) if not minify_png_options.pngquant_enabled else None,
                str(input_file) if not minify_png_options.pngquant_enabled else str(output_file),
            ]
            if utils.run_subprocess(cmd=oxipng_cmd) != 0:
                output_file.unlink(missing_ok=True)
                return None

        is_new_smaller = utils.is_new_smaller(
            old_file=input_file, new_file=output_file, blog_config=blog_config
        )
        if is_new_smaller:
            return cached_file
        else:
            log.debug(
                f"Minified file larger than original: "
                f"{cached_file.original_file_path} (removing cached file)"
            )
            output_file.unlink()
    except FileNotFoundError as e:
        log.warning(e)

    return None


def _minify_with_cache(file: Path, blog_config: BlogConfig, minify_method, semaphore: Semaphore):
    recreate_file = False
    if str(file) in blog_config.cached_files:
        file_hash = utils.calculate_file_hash(file=(blog_config.site_dir / file))
        cached_file = blog_config.cached_files[str(file)]
        if cached_file.original_file_hash == file_hash:
            cached_file_name = blog_config.cache_dir / cached_file.cached_file_name
            if cached_file_name.exists():
                utils.copy_cached_file(cached_file=cached_file, blog_config=blog_config)
            else:
                recreate_file = True
        else:
            recreate_file = True
    else:
        cached_file = CachedFile()
        cached_file.based_on(file=file, directory=blog_config.site_dir)
        recreate_file = True

    if recreate_file:
        log.debug(f"Minifying file: {file} (putting into cache)")
        cached_file = minify_method(cached_file=cached_file, blog_config=blog_config)
        if cached_file:
            blog_config.cached_files[str(cached_file.original_file_path)] = cached_file
            utils.copy_cached_file(cached_file=cached_file, blog_config=blog_config)
    else:
        log.debug(f"File already minified: {file} (retrieving from cache)")
    semaphore.release()


def _build_minification_threads(
    blog_config: BlogConfig, extensions: List[str], minify_method, semaphore: Semaphore
) -> List[Thread]:
    threads = []

    for file in utils.list_files(
        directory=blog_config.site_dir, extensions=extensions, relative_to=blog_config.site_dir
    ):
        semaphore.acquire()
        thread = Thread(
            target=_minify_with_cache,
            kwargs={
                "file": file,
                "blog_config": blog_config,
                "minify_method": minify_method,
                "semaphore": semaphore,
            },
        )
        thread.start()
        threads.append(thread)
    return threads


def post_build_files_minification(blog_config: BlogConfig):
    # TODO: Add path to tools checker

    minify_options = blog_config.plugin_config.minify

    cached_files_list: Path = blog_config.cache_dir / minify_options.cache_file
    if cached_files_list.exists():
        try:
            with open(cached_files_list, "r") as yaml_file:
                cached_files = yaml.safe_load(yaml_file)
                for file_path, cached_file in cached_files.items():
                    blog_config.cached_files[file_path] = CachedFile(**cached_file)
        except (yaml.YAMLError, AttributeError) as e:
            log.warning(f"File '{cached_files_list}' corrupted. Rebuilding cache.")
            log.debug(e)

    if minify_options.threads < 1:
        log.critical("Number of 'threads' cannot be smaller than 1")
        exit(1)

    # Multi threading of file optimization process
    semaphore = Semaphore(minify_options.threads)
    threads = []

    if blog_config.plugin_config.minify.png.enabled:
        log.info("Optimizing PNG graphics files")
        threads.extend(
            _build_minification_threads(
                blog_config=blog_config,
                extensions=[".png"],
                minify_method=_png_minifier,
                semaphore=semaphore,
            )
        )

    if blog_config.plugin_config.minify.jpg.enabled:
        log.info("Optimizing JPG graphics files")
        threads.extend(
            _build_minification_threads(
                blog_config=blog_config,
                extensions=[".jpg", ".jpeg"],
                minify_method=_jpg_minifier,
                semaphore=semaphore,
            )
        )

    if blog_config.plugin_config.minify.svg.enabled:
        log.info("Optimizing SVG graphics files")
        threads.extend(
            _build_minification_threads(
                blog_config=blog_config,
                extensions=[".svg"],
                minify_method=_svg_minifier,
                semaphore=semaphore,
            )
        )

    # Wait for all threads to be finished
    for thread in threads:
        thread.join()

    cached_files_for_yaml = {}
    for file_name, cached_file in blog_config.cached_files.items():
        # TODO: Cleanup yaml from unused/deleted files and delete those that are unused
        cached_file = {k: str(v) for k, v in cached_file.as_dict.items()}
        cached_files_for_yaml[file_name] = cached_file

    with open(cached_files_list, "w") as yaml_file:
        yaml.safe_dump(cached_files_for_yaml, yaml_file)
