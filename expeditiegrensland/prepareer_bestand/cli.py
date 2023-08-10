#!/usr/bin/env python3

import argparse
from textwrap import dedent

from ..gemeenschappelijk.arg_types import bestaand_bestand, slak
from ..gemeenschappelijk.maak_cli import maak_cli
from . import prepareer_bestand
from .converteerders import (
    achtergrond_converteerder_fabriek,
    afbeelding_bijlage_converteerder_fabriek,
    audio_bijlage_converteerder_fabriek,
    film_converteerder_fabriek,
    video_bijlage_converteerder_fabriek,
)
from .noemers import (
    achtergrond_noemer_fabriek,
    citaat_afbeelding_noemer_fabriek,
    citaat_audio_noemer_fabriek,
    citaat_video_noemer_fabriek,
    film_noemer_fabiek,
    verhaal_afbeelding_noemer_fabriek,
    verhaal_audio_noemer_fabriek,
    verhaal_video_noemer_fabriek,
    woord_afbeelding_noemer_fabriek,
    woord_audio_noemer_fabriek,
    woord_video_noemer_fabriek,
)


def configureer_parser(parser: argparse.ArgumentParser):
    subparsers = parser.add_subparsers(
        title="Soort",
        description=dedent(
            """
            Het soort bestand om te prepareren. Om de extra opties te bekijken per type, gebruik:
              eg-prepareer-bestand {film,achtergrond,bijlage} -h
            """
        ).strip(),
        dest="soort",
        required=True,
    )

    #
    # Parser voor films
    #

    film_parser = subparsers.add_parser(
        "film",
        help="Film van een expeditie",
        allow_abbrev=False,
        formatter_class=argparse.RawTextHelpFormatter,
    )

    film_parser.add_argument(
        "slak",
        type=slak,
        help=dedent(
            """
            Korte naam (letters en streepjes) van de expeditie
              Kies '-' om de bestandsnaam van de invoer te gebruiken
            """
        ).strip(),
    )

    film_parser.add_argument(
        "invoer",
        nargs="+",
        type=bestaand_bestand,
        help="Invoerbestand om om te zetten en te prepareren",
    )

    #
    # Parser voor achtergronden
    #

    achtergrond_parser = subparsers.add_parser(
        "achtergrond",
        help="Achtergrondafbeelding voor een expeditie",
        allow_abbrev=False,
        formatter_class=argparse.RawTextHelpFormatter,
    )

    achtergrond_parser.add_argument(
        "slak",
        type=slak,
        help=dedent(
            """
            Korte naam (letters en streepjes) van de expeditie
              Kies '-' om de bestandsnaam van de invoer te gebruiken
            """
        ).strip(),
    )

    achtergrond_parser.add_argument(
        "invoer",
        nargs="+",
        type=bestaand_bestand,
        help="Invoerbestand om om te zetten en te prepareren",
    )

    #
    # Parser voor bijlagen
    #

    bijlage_parser = subparsers.add_parser(
        "bijlage",
        help="Bijlage bij een woord, citaat of expeditieverhaal",
        allow_abbrev=False,
        formatter_class=argparse.RawTextHelpFormatter,
    )

    bijlage_parser.add_argument(
        "itemtype",
        choices=["woord", "citaat", "verhaal"],
        help="Type item waar de bijlage bijhoort",
    )

    bijlage_parser.add_argument(
        "formaat",
        choices=["afbeelding", "video", "audio"],
        help="Type formaat van het bestand",
    )

    bijlage_parser.add_argument(
        "slak",
        type=slak,
        help=dedent(
            """
            Korte naam (letters en streepjes) van het woord, citaat of expeditieverhaal
              Kies '-' om de bestandsnaam van de invoer te gebruiken
            """
        ).strip(),
    )

    bijlage_parser.add_argument(
        "invoer",
        nargs="+",
        type=bestaand_bestand,
        help="Invoerbestand om om te zetten en te prepareren",
    )


def converteer_opties(opties: argparse.Namespace):
    converteerder = None
    naam = None

    match opties.soort:
        case "film":
            converteerder = film_converteerder_fabriek()
            naam = film_noemer_fabiek(opties.slak)

        case "achtergrond":
            converteerder = achtergrond_converteerder_fabriek()
            naam = achtergrond_noemer_fabriek(opties.slak)

        case "bijlage":
            match opties.formaat:
                case "afbeelding":
                    converteerder = afbeelding_bijlage_converteerder_fabriek()
                    match opties.itemtype:
                        case "woord":
                            naam = woord_afbeelding_noemer_fabriek(opties.slak)
                        case "citaat":
                            naam = citaat_afbeelding_noemer_fabriek(opties.slak)
                        case "verhaal":
                            naam = verhaal_afbeelding_noemer_fabriek(opties.slak)
                        case _:
                            pass

                case "video":
                    converteerder = video_bijlage_converteerder_fabriek()
                    match opties.itemtype:
                        case "woord":
                            naam = woord_video_noemer_fabriek(opties.slak)
                        case "citaat":
                            naam = citaat_video_noemer_fabriek(opties.slak)
                        case "verhaal":
                            naam = verhaal_video_noemer_fabriek(opties.slak)
                        case _:
                            pass

                case "audio":
                    converteerder = audio_bijlage_converteerder_fabriek()
                    match opties.itemtype:
                        case "woord":
                            naam = woord_audio_noemer_fabriek(opties.slak)
                        case "citaat":
                            naam = citaat_audio_noemer_fabriek(opties.slak)
                        case "verhaal":
                            naam = verhaal_audio_noemer_fabriek(opties.slak)
                        case _:
                            pass
                case _:
                    pass

        case _:
            pass

    if not naam:
        raise RuntimeError("Kan geen geldige noemer vinden")

    if not converteerder:
        raise RuntimeError("Kan geen geldige converteerder vinden")

    return prepareer_bestand.PrepareerBestandOpties(
        invoer=opties.invoer, converteerder=converteerder, noemer=naam
    )


def main():
    maak_cli(
        naam="eg-prepareer-bestand",
        beschrijving=prepareer_bestand.__doc__,
        configureer_parser=configureer_parser,
        vereiste_programmas=["ffmpeg"],  # FIXME: Voeg alle benodigde programmas toe
        converteer_opties=converteer_opties,
        draaier=prepareer_bestand.prepareer_bestand,
    )


if __name__ == "__main__":
    main()
