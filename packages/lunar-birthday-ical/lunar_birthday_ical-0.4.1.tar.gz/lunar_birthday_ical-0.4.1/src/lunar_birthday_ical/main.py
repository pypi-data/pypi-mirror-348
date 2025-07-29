#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK
# author: ak1ra
# date: 2025-01-24

import argparse
import time
from pathlib import Path

import argcomplete
from lunar_python import Lunar, Solar

from lunar_birthday_ical.icalendar import create_calendar
from lunar_birthday_ical.logging import setup_logger

logger = setup_logger(__name__, "messages.log")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate iCal events and reminders for lunar birthday and cycle days."
    )
    parser.add_argument(
        "config_files",
        type=Path,
        nargs="*",
        metavar="config.yaml",
        help="config file for iCal, checkout config/example-lunar-birthday.yaml for example.",
    )

    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "-L",
        "--lunar-to-solar",
        type=int,
        nargs=3,
        metavar=("YYYY", "MM", "DD"),
        help="Convert lunar date to solar date, add minus sign before leap lunar month.",
    )
    group.add_argument(
        "-S",
        "--solar-to-lunar",
        type=int,
        nargs=3,
        metavar=("YYYY", "MM", "DD"),
        help="Convert solar date to lunar date.",
    )

    argcomplete.autocomplete(parser)
    args = parser.parse_args()

    if args.lunar_to_solar:
        lunar = Lunar.fromYmd(*args.lunar_to_solar)
        solar = lunar.getSolar()
        logger.info("Lunar date %s is Solar %s", lunar.toString(), solar.toString())
        parser.exit()

    if args.solar_to_lunar:
        solar = Solar.fromYmd(*args.solar_to_lunar)
        lunar = solar.getLunar()
        logger.info("Solar date %s is Lunar %s", solar.toString(), lunar.toString())
        parser.exit()

    if len(args.config_files) == 0:
        parser.print_help()
        parser.exit()

    for config_file in args.config_files:
        logger.debug("loading config file %s", config_file)
        start = time.perf_counter()
        create_calendar(Path(config_file))
        elapsed = time.perf_counter() - start
        logger.debug("iCal generation elapsed at %.6fs for %s", elapsed, config_file)


if __name__ == "__main__":
    main()
