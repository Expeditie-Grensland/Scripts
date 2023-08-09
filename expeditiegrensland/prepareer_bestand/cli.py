#!/usr/bin/env python3

import argparse
from textwrap import dedent

from matplotlib.pyplot import switch_backend

from ..gemeenschappelijk.arg_types import bestaand_bestand, lege_map, slak
from ..gemeenschappelijk.maak_cli import maak_cli
from .converteerders.achtergrond import AchtergrondConverteerder
from .converteerders.afbeelding_bijlage import AfbeeldingBijlageConverteerder
from .converteerders.audio_bijlage import AudioBijlageConverteerder
from .converteerders.film import FilmConverteerder
from .converteerders.video_bijlage import VideoBijlageConverteerder
from .noemers.achtergrond import AchtergrondNoemer
from .noemers.citaat_bijlage import CitaatBijlageNoemer
from .noemers.film import FilmNoemer
from .noemers.verhaal_bijlage import VerhaalBijlageNoemer
from .noemers.woord_bijlage import WoordBijlageNoemer
from .prepareer_bestand import PrepareerBestandOpties


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


def converteer_opties(opties: argparse.Namespace) -> PrepareerBestandOpties:
    if opties.soort == "film":
        converteerder = FilmConverteerder()
    elif opties.soort == "achtergrond":
        converteerder = AchtergrondConverteerder()
    elif opties.soort == "bijlage" and opties.formaat == "afbeelding":
        converteerder = AfbeeldingBijlageConverteerder()
    elif opties.soort == "bijlage" and opties.formaat == "video":
        converteerder = VideoBijlageConverteerder()
    elif opties.soort == "bijlage" and opties.formaat == "audio":
        converteerder = AudioBijlageConverteerder()
    else:
        raise RuntimeError("Kan geen geldige converteerder vinden")

    if opties.soort == "film":
        noemer = FilmNoemer()
    elif opties.soort == "achtergrond":
        noemer = AchtergrondNoemer()
    elif opties.soort == "bijlage" and opties.itemtype == "woord":
        noemer = WoordBijlageNoemer
    elif opties.soort == "bijlage" and opties.itemtype == "citaat":
        noemer = CitaatBijlageNoemer
    elif opties.soort == "bijlage" and opties.itemtype == "verhaal":
        noemer = VerhaalBijlageNoemer
    else:
        raise RuntimeError("Kan geen geldige noemer vinden")

    return PrepareerBestandOpties(converteerder=converteerder, noemer=noemer)


def main():
    maak_cli(
        naam="eg-prepareer-bestand",
        beschrijving=None,  # FIXME
        configureer_parser=configureer_parser,
        vereiste_programmas=["ffmpeg"],  # FIXME
        converteer_opties=converteer_opties,
        draaier=None,  # FIXME
    )


if __name__ == "__main__":
    main()
