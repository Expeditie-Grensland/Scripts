#!/usr/bin/env python3

import argparse

from ..gemeenschappelijk.arg_types import bestaand_bestand, lege_map
from ..gemeenschappelijk.maak_cli import maak_cli
from .configs.film import video2dash_film_config
from .video2dash import Video2DashOpties
from .video2dash import __doc__ as doc_str
from .video2dash import video2dash


def configureer_parser(parser: argparse.ArgumentParser):
    config = parser.add_mutually_exclusive_group()

    config.set_defaults(config="film")

    config.add_argument(
        "--film",
        dest="config",
        action="store_const",
        const="film",
        help="Gebruik configuratiebestand voor films (standaard)",
    )

    parser.add_argument(
        "--max-resolutie",
        type=int,
        default=1080,
        help="Maximale resolutie (in verticale pixels) om bestanden in te produceren (standaard: %(default)s)",
        metavar="HOOGTE",
    )

    parser.add_argument(
        "--beeldsnelheid",
        type=int,
        default=60,
        help="Beeldsnelheid van het invoer videobestand (standaard: %(default)s)",
        metavar="BPS",
    )

    parser.add_argument(
        "invoer",
        type=bestaand_bestand,
        help="Videobestand dat omgezet dient te worden",
    )

    parser.add_argument(
        "uitvoer",
        type=lege_map,
        help="Map om omgezette bestanden in op te slaan (dient leeg of afwezig te zijn)",
    )


def converteer_opties(opties: argparse.Namespace) -> Video2DashOpties:
    if opties.config == "film":
        config = video2dash_film_config
    else:
        raise RuntimeError("Geen geldige config gevonden")

    return Video2DashOpties(
        invoer=opties.invoer,
        uitvoer=opties.uitvoer,
        max_resolutie=opties.max_resolutie,
        beeldsnelheid=opties.beeldsnelheid,
        config=config,
    )


def main():
    maak_cli(
        naam="eg-video2dash",
        beschrijving=doc_str,
        configureer_parser=configureer_parser,
        converteer_opties=converteer_opties,
        draaier=video2dash,
    )


if __name__ == "__main__":
    main()
