import traceback
from argparse import ArgumentParser, Namespace, RawTextHelpFormatter
from collections.abc import Callable
from logging import getLogger

import coloredlogs


def maak_cli(
    *,
    naam: str,
    beschrijving: str,
    configureer_parser: Callable[[ArgumentParser], None],
    draai_module: Callable[[Namespace], None],
):
    logger = getLogger("__main__")

    parser = ArgumentParser(
        prog=naam,
        description=beschrijving,
        allow_abbrev=False,
        formatter_class=RawTextHelpFormatter,
    )

    configureer_parser(parser)

    parser.add_argument(
        "--debug",
        action="store_true",
        help="Schrijf foutopsporingsinformatie naar de terminal",
    )

    opties = parser.parse_args()

    print()
    coloredlogs.install(
        logger=logger,
        fmt="%(asctime)s %(levelname)s %(message)s\n",
        level=("DEBUG" if opties.debug else "INFO"),
    )

    logger.debug(f"Ruwe opties:\n{opties}")

    try:
        draai_module(opties)
    except Exception as error:
        logger.critical(error)
        logger.debug(
            "Tracering:\n"
            + "".join(traceback.format_list(traceback.extract_tb(error.__traceback__)))
        )
