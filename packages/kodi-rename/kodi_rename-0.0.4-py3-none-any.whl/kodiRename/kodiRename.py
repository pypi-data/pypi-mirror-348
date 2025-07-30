# -*- coding: utf-8 -*-
#################################################################################
# MIT License
#
# Copyright (c) 2025 Duncan Fraser
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
#################################################################################
#
# File          : kodiRename.py
#
# Author        : Duncan Fraser <dfraser@thedrunkencoder.uk>
#
# Description   :
#
#################################################################################
import logging
import os
import sys
from argparse import ArgumentParser
from typing import Final, Optional

from alive_progress import alive_bar

from . import collector, config, process

DEFAULT_CONFIG_FILE: Final = "config.ini"
OUTPUT_MOVIES: Final = "movie.bin"
OUTPUT_TV: Final = "tv.bin"


def collectConfig(config_path: str = DEFAULT_CONFIG_FILE) -> config.ConfigSpec:
    config_data = config.ConfigSpec()

    if not os.path.exists(config_path):
        return config_data

    with open(config_path, "rb") as conf_file:
        config_data = config.parseConfig(configIO=conf_file)

    return config_data


def configLogger(
    level: str, log_file: Optional[str] = None, log_std: bool = False
) -> logging.Logger:

    logger = logging.getLogger(__name__)
    form = logging.Formatter(
        "%(asctime)s %(levelname)s [%(module)s:%(funcName)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    log_levels = {
        "debug": logging.DEBUG,
        "info": logging.INFO,
        "warning": logging.WARNING,
        "error": logging.ERROR,
        "critical": logging.CRITICAL,
    }

    if level not in log_levels:
        raise ValueError("Undefined Level {0}".format(level))

    logger.setLevel(log_levels[level])

    if log_file:
        fh = logging.FileHandler(filename=log_file, mode="a")
        fh.setFormatter(form)
        logger.addHandler(fh)

    if log_std:
        sh = logging.StreamHandler(sys.stdout)
        sh.setFormatter(form)
        logger.addHandler(sh)

    return logger


def parseArgs(config_data: config.ConfigSpec):
    desc_str = ""
    parser = ArgumentParser(prog="kodiRename", description=desc_str)

    parser.add_argument("--config", "-c", required=False, default=DEFAULT_CONFIG_FILE)
    parser.add_argument(
        "--debug",
        "-d",
        action="store",
        default="info",
        choices=["debug", "info", "warning", "error", "critical"],
        required=False,
    )
    parser.add_argument("--logfile", action="store", required=False, metavar="xxx.log")
    parser.add_argument(
        "--quiet", "-q", action="store_true", required=False, default=False
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    init = subparsers.add_parser("init", help="Initialize config file")  # noqa: F841
    collection = subparsers.add_parser(  # noqa: F841
        "collect", help="Collect Information"
    )
    rename = subparsers.add_parser("rename", help="Use Information")
    clean = subparsers.add_parser("clean", help="Print Information")

    rename.add_argument("--dryRun", required=False, action="store_true")
    clean.add_argument("--dryRun", required=False, action="store_true")

    args = parser.parse_args()

    if args.config:
        config_data = collectConfig(args.config)

    if args.logfile:
        config_data.general.logFile = args.logfile

    return (args, config_data)


def init(config_path: str = DEFAULT_CONFIG_FILE) -> int:
    with open(config_path, "w") as conf_file:
        config.writeDefaultConfig(configIO=conf_file)
    return 0


def collect(config_data: config.ConfigSpec) -> int:
    movie_info = collector.getMovieInfo(config=config_data)
    tv_info = collector.getTvInfo(config=config_data)

    if not os.path.isdir(config_data.general.dataDirectory):
        os.makedirs(config_data.general.dataDirectory, exist_ok=True)

    with open(
        os.path.join(config_data.general.dataDirectory, OUTPUT_MOVIES), "wb"
    ) as movie_file:
        collector.serializeMovieInfo(pickleIO=movie_file, movieInfo=movie_info)

    with open(
        os.path.join(config_data.general.dataDirectory, OUTPUT_TV), "wb"
    ) as tv_file:
        collector.serializeTVInfo(pickleIO=tv_file, tvInfo=tv_info)

    return 0


def rename(config_data: config.ConfigSpec, dry_run: bool = False) -> int:
    with open(
        os.path.join(config_data.general.dataDirectory, OUTPUT_MOVIES), "rb"
    ) as movie_file:
        movie_info = collector.deserializeMovieInfo(pickleIO=movie_file)

    with open(
        os.path.join(config_data.general.dataDirectory, OUTPUT_TV), "rb"
    ) as tv_file:
        tv_info = collector.deserializeTVInfo(pickleIO=tv_file)

    movie_rename = process.collectMovieRename(config=config_data, movie_list=movie_info)
    tv_rename = process.collectTvRename(config=config_data, tv_info=tv_info)

    with alive_bar(len(movie_rename), title="Movie Rename") as progress:
        for movie in movie_rename:
            config_data.log.info(
                "{2} Movie   : {0} --> {1}".format(
                    movie.src.path,
                    movie.dest.path,
                    "Moving" if config_data.general.mode == "move" else "Copying",
                )
            )
            process.performRenameOperation(
                config=config_data, data=movie, dry_run=dry_run
            )
            progress()

    with alive_bar(len(tv_rename), title="TV Rename   ") as progress:
        for tv in tv_rename:
            config_data.log.info(
                "{2} Episode : {0} --> {1}".format(
                    tv.src.path,
                    tv.dest.path,
                    "Moving" if config_data.general.mode == "move" else "Copying",
                )
            )

            process.performRenameOperation(config=config_data, data=tv, dry_run=dry_run)
            progress()

    return 0


def clean(config_data: config.ConfigSpec, dry_run: bool = False) -> int:
    with open(
        os.path.join(config_data.general.dataDirectory, OUTPUT_MOVIES), "rb"
    ) as movie_file:
        movie_info = collector.deserializeMovieInfo(pickleIO=movie_file)

    with open(
        os.path.join(config_data.general.dataDirectory, OUTPUT_TV), "rb"
    ) as tv_file:
        tv_info = collector.deserializeTVInfo(pickleIO=tv_file)

    movie_rename = process.collectMovieRename(config=config_data, movie_list=movie_info)
    tv_rename = process.collectTvRename(config=config_data, tv_info=tv_info)

    with alive_bar(len(movie_rename), title="Movie Clean") as progress:
        for movie in movie_rename:
            config_data.log.info(
                "Deleting Movie Directory : {0}".format(movie.src.parentPath)
            )
            process.performCleanDirectory(
                config=config_data, data=movie, dry_run=dry_run
            )
            progress()

    with alive_bar(len(tv_rename), title="TV Clean   ") as progress:
        for tv in tv_rename:
            config_data.log.info(
                "Deleting TV Directory    : {0}".format(tv.src.parentPath)
            )
            process.performCleanDirectory(config=config_data, data=tv, dry_run=dry_run)
            progress()
    return 0


def main() -> int:
    config_data = collectConfig(DEFAULT_CONFIG_FILE)

    args, config_data = parseArgs(config_data=config_data)

    if not os.path.isdir(config_data.general.dataDirectory):
        os.makedirs(config_data.general.dataDirectory, exist_ok=True)

    if not os.path.isdir(os.path.dirname(config_data.general.logFile)):
        if os.path.dirname(config_data.general.logFile) != "":
            os.makedirs(os.path.dirname(config_data.general.logFile), exist_ok=True)

    logger = configLogger(
        level=args.debug, log_file=config_data.general.logFile, log_std=(not args.quiet)
    )
    config_data.log = logger

    status = 0

    if args.command == "init":
        status = init(args.config)
    elif args.command == "collect":
        status = collect(config_data=config_data)
    elif args.command == "rename":
        status = rename(config_data=config_data, dry_run=args.dryRun)
    elif args.command == "clean":
        status = clean(config_data=config_data, dry_run=args.dryRun)

    return status


if __name__ == "__main__":
    sys.exit(main())
