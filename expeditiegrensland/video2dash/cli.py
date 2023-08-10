#!/usr/bin/env python3

import argparse

from . import video2dash
from ..gemeenschappelijk.maak_cli import maak_cli
from ..gemeenschappelijk.arg_types import bestaand_bestand, lege_map


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

    config.add_argument(
        "--config",
        dest="config_bestand",
        type=bestaand_bestand,
        help="Gebruik een ander configuratiebestand",
        metavar="BESTAND",
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


def converteer_opties(opties: argparse.Namespace) -> video2dash.Video2DashOpties:
    if opties.config_bestand:
        config_bestand = video2dash.ConfigBestandExtern(opties.config_bestand)
    else:
        config_bestand = video2dash.ConfigBestandIngebouwd(opties.config)

    return video2dash.Video2DashOpties(
        invoer=opties.invoer,
        uitvoer=opties.uitvoer,
        max_resolutie=opties.max_resolutie,
        beeldsnelheid=opties.beeldsnelheid,
        config_bestand=config_bestand,
        debug=opties.debug,
    )


def main():
    maak_cli(
        naam="eg-video2dash",
        beschrijving=video2dash.__doc__,
        configureer_parser=configureer_parser,
        converteer_opties=converteer_opties,
        draaier=video2dash.video2dash,
    )


if __name__ == "__main__":
    main()
