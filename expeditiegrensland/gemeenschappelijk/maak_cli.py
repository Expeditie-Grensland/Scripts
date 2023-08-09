import argparse
import logging
import traceback
from collections.abc import Callable
from typing import TypeVar

import coloredlogs
from expeditiegrensland.gemeenschappelijk.commando import vereis_programma

T = TypeVar("T")


def maak_cli(
    *,
    naam: str,
    beschrijving: str,
    configureer_parser: Callable[[argparse.ArgumentParser], None],
    converteer_opties: Callable[[argparse.Namespace], T],
    vereiste_programmas: list[str] = [],
    draaier: Callable[[T], None],
) -> tuple[argparse.Namespace, logging.Logger]:
    logger = logging.getLogger("__main__")

    parser = argparse.ArgumentParser(
        prog=naam,
        description=beschrijving,
        allow_abbrev=False,
        formatter_class=argparse.RawTextHelpFormatter,
    )

    configureer_parser(parser)

    parser.add_argument(
        "--debug",
        action="store_true",
        help="Schrijf foutopsporingsinformatie naar de terminal",
    )

    ruwe_opties = parser.parse_args()

    print()
    coloredlogs.install(
        logger=logger,
        fmt="%(asctime)s %(levelname)s %(message)s\n",
        level=("DEBUG" if ruwe_opties.debug else "INFO"),
    )

    logger.debug(f"Ruwe opties:\n{ruwe_opties}")

    try:
        for programma in vereiste_programmas:
            vereis_programma(programma)

        opties = converteer_opties(ruwe_opties)
        logger.debug(f"Opties:\n{opties}")

        draaier(opties)
    except Exception as error:
        logger.critical(error)
        logger.debug(
            "Tracering:\n"
            + "".join(traceback.format_list(traceback.extract_tb(error.__traceback__)))
        )
