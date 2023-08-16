#!/usr/bin/env python3

from argparse import ArgumentParser, Namespace, RawTextHelpFormatter
from textwrap import dedent

from ..gemeenschappelijk.arg_types import bestaand_bestand, een_map, slak
from ..gemeenschappelijk.maak_cli import maak_cli
from .acties import kopieer_actie_fabriek, upload_actie_fabriek, verplaats_actie_fabriek
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
from .prepareer_bestand import prepareer_bestand


def configureer_parser(parser: ArgumentParser):
    actie_groep = parser.add_argument_group(
        title="Actie",
        description="De actie om uit te voeren voor het geconverteerde en genoemde bestand",
    )
    actie_exclusief = actie_groep.add_mutually_exclusive_group(required=True)

    actie_exclusief.add_argument(
        "--upload",
        metavar="EMMER[/MAP]",
        help=dedent(
            """
            Upload het bestand naar S3 in de gegeven emmer (en map).
            Zorg dat inloggegevens beschikbaar zijn voor Boto3
            (via een configuratiebestand of omgevingsvariabelen):
            https://boto3.amazonaws.com/v1/documentation/api/latest/guide/configuration.html
        """
        ).strip(),
    )

    actie_exclusief.add_argument(
        "--verplaats",
        type=een_map,
        metavar="UITVOER_MAP",
        help="Verplaats het bestand naar de gegeven map",
    )

    actie_exclusief.add_argument(
        "--kopieer",
        type=een_map,
        metavar="UITVOER_MAP",
        help="Kopieer het bestand naar de gegeven map",
    )

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
        formatter_class=RawTextHelpFormatter,
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
        formatter_class=RawTextHelpFormatter,
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
        formatter_class=RawTextHelpFormatter,
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


def draai_module(opties: Namespace):
    converteerder = None
    noemer = None

    match opties.soort:
        case "film":
            converteerder = film_converteerder_fabriek()
            noemer = film_noemer_fabiek(opties.slak)

        case "achtergrond":
            converteerder = achtergrond_converteerder_fabriek()
            noemer = achtergrond_noemer_fabriek(opties.slak)

        case "bijlage":
            match opties.formaat:
                case "afbeelding":
                    converteerder = afbeelding_bijlage_converteerder_fabriek()
                    match opties.itemtype:
                        case "woord":
                            noemer = woord_afbeelding_noemer_fabriek(opties.slak)
                        case "citaat":
                            noemer = citaat_afbeelding_noemer_fabriek(opties.slak)
                        case "verhaal":
                            noemer = verhaal_afbeelding_noemer_fabriek(opties.slak)
                        case _:
                            pass

                case "video":
                    converteerder = video_bijlage_converteerder_fabriek()
                    match opties.itemtype:
                        case "woord":
                            noemer = woord_video_noemer_fabriek(opties.slak)
                        case "citaat":
                            noemer = citaat_video_noemer_fabriek(opties.slak)
                        case "verhaal":
                            noemer = verhaal_video_noemer_fabriek(opties.slak)
                        case _:
                            pass

                case "audio":
                    converteerder = audio_bijlage_converteerder_fabriek()
                    match opties.itemtype:
                        case "woord":
                            noemer = woord_audio_noemer_fabriek(opties.slak)
                        case "citaat":
                            noemer = citaat_audio_noemer_fabriek(opties.slak)
                        case "verhaal":
                            noemer = verhaal_audio_noemer_fabriek(opties.slak)
                        case _:
                            pass
                case _:
                    pass

        case _:
            pass

    if not noemer:
        raise RuntimeError("Kan geen geldige noemer vinden")

    if not converteerder:
        raise RuntimeError("Kan geen geldige converteerder vinden")

    actie = None

    if opties.upload:
        actie = upload_actie_fabriek(opties.upload)
    elif opties.verplaats:
        actie = verplaats_actie_fabriek(opties.verplaats)
    elif opties.kopieer:
        actie = kopieer_actie_fabriek(opties.kopieer)

    if not actie:
        raise RuntimeError("Kan geen geldige actie vinden")

    prepareer_bestand(
        invoer=opties.invoer,
        converteerder=converteerder,
        noemer=noemer,
        actie=actie,
    )


def main():
    maak_cli(
        naam="eg-prepareer-bestand",
        beschrijving="Prepareer (converteer, hernoem & upload) een bestand voor gebruik op de website",
        configureer_parser=configureer_parser,
        draai_module=draai_module,
        voorbeelden=[
            "eg-prepareer-bestand --upload eg-media film noordkaap noordkaap-movie.mp4",
            "eg-prepareer-bestand --upload eg-media achtergrond - *.jpg",
            "eg-prepareer-bestand --verplaats ./media bijlage woord audio - kapot.mp3"
        ],
    )


if __name__ == "__main__":
    main()
