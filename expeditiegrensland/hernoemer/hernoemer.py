#!/usr/bin/env python3

"""Hernoem (en upload) een bestand voor gebruik op de website"""

import argparse
import logging
import os
import shutil
import sys
from textwrap import dedent

import boto3

import expeditiegrensland.gemeenschappelijk.arg_types as eg_arg_types
import expeditiegrensland.gemeenschappelijk.commando as eg_commando
import expeditiegrensland.gemeenschappelijk.log as eg_log

logger = logging.getLogger("eg-hernoemer")


def lees_opties():
    parser = argparse.ArgumentParser(
        prog="eg-hernoemer",
        description=sys.modules[__name__].__doc__,
        allow_abbrev=False,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=dedent(
            """
            Voorbeelden:
              eg-hernoemer --expeditie-film stans --upload eg-media ffmpeg-output
              eg-hernoemer --citaat-bijlage bier-gefunden --kopieer eg-map video.mp4
              eg-hernoemer --expeditie-film %naam% --verplaats eg-map balkan.jpg moi.jpg
            """
        ),
    )

    type_groep = parser.add_argument_group("Type van bestand")
    type_exclusief = type_groep.add_mutually_exclusive_group(required=True)

    type_exclusief.add_argument(
        "--expeditie-film",
        dest="naam",
        type=lambda x: os.path.join(x, "film"),
        metavar="EXPEDITIE",
        help="Film van de gegeven expeditie",
    )

    type_exclusief.add_argument(
        "--expeditie-achtergrond",
        dest="naam",
        type=lambda x: os.path.join(x, "achtergrond"),
        metavar="EXPEDITIE",
        help="Achtergrond van de gegeven expeditie",
    )

    type_exclusief.add_argument(
        "--expeditie-verhaal",
        dest="naam",
        type=lambda x: os.path.join(x, "verhaal"),
        metavar="EXPEDITIE",
        help="Bijlage voor verhaal van de gegeven expeditie",
    )

    type_exclusief.add_argument(
        "--woordenboek-bijlage",
        dest="naam",
        type=lambda x: os.path.join("woordenboek", x),
        metavar="WOORD",
        help="Bijlage bij het gegeven woord",
    )

    type_exclusief.add_argument(
        "--citaat-bijlage",
        dest="naam",
        type=lambda x: os.path.join("citaten", x),
        metavar="CITAAT",
        help="Bijlage bij het gegeven citaat",
    )

    actie_groep = parser.add_argument_group("Uit te voeren actie")
    actie_exclusief = actie_groep.add_mutually_exclusive_group(required=False)

    actie_exclusief.set_defaults(actie=("geen",))

    actie_exclusief.add_argument(
        "--upload",
        dest="actie",
        type=lambda x: ("upload", x),
        metavar="EMMER[/MAP]",
        help="""
            Upload het bestand naar S3 in de gegeven emmer (en map).
            Zorg dat inloggegevens beschikbaar zijn voor Boto3
            (via een configuratiebestand of omgevingsvariabelen):
            https://boto3.amazonaws.com/v1/documentation/api/latest/guide/configuration.html
        """,
    )

    actie_exclusief.add_argument(
        "--verplaats",
        dest="actie",
        type=lambda x: ("verplaats", eg_arg_types.een_map(x)),
        metavar="UITVOER_MAP",
        help="Hernoem het bestand en verplaats het naar de gegeven map",
    )

    actie_exclusief.add_argument(
        "--kopieer",
        dest="actie",
        type=lambda x: ("kopieer", eg_arg_types.een_map(x)),
        metavar="UITVOER_MAP",
        help="Hernoem het bestand en kopieer het naar de gegeven map",
    )

    actie_exclusief.add_argument(
        "--hernoem",
        dest="actie",
        action="store_const",
        const=("hernoem",),
        help="Hernoem het bestand zonder het te verplaatsen",
    )

    parser.add_argument(
        "--debug",
        action="store_true",
        help="Schrijf foutopsporingsinformatie naar de terminal",
    )

    parser.add_argument(
        "invoer",
        type=eg_arg_types.bestaand_pad,
        help="Bestand of map die moeten worden hernoemd",
    )

    return parser.parse_args()


def lees_hash(pad):
    if os.path.isdir(pad):
        hash_commando = [
            ["tar", "-c", "-f", "-", "-C", pad, "--sort=name", "."],
            ["sha1sum"],
        ]
    else:
        hash_commando = [["sha1sum", pad]]

    hash = eg_commando.draai_pijp(hash_commando, logger).split(" ")[0][:8]

    return hash


def hernoem(invoer_pad, opties):
    logger.info(f"Bestand:\n{invoer_pad}")

    naam, extensie = os.path.splitext(os.path.basename(invoer_pad))
    logger.debug(f"Oude bestandsnaam:\n{naam}")
    logger.debug(f"Extensie:\n{extensie}")

    nieuwe_naam = f"{opties.naam}.{lees_hash(invoer_pad)}{extensie}".replace(
        "%naam%", naam
    )

    actie, param = opties.actie


    if actie == "upload":
        emmer, *emmer_pad = param.split("/", 1) + [""]
        emmer_pad = emmer_pad[0]
        logger.info(f"Bestand wordt geüpload naar emmer:\n{emmer}")

        object_naam = os.path.join(emmer_pad, nieuwe_naam).replace(os.path.sep, "/")
        logger.info(f"Bestand wordt geüpload als:\n{object_naam}")

        s3_klant = boto3.client("s3")
        s3_klant.upload_file(invoer_pad, emmer, object_naam)

    if actie == "verplaats":
        nieuw_pad = os.path.join(param, nieuwe_naam)
        nieuwe_map = os.path.dirname(nieuw_pad)

        if not os.path.isdir(nieuwe_map):
            logger.info(f"Map wordt aangemaakt:\n{nieuwe_map}")
            os.makedirs(nieuwe_map)

        shutil.move(invoer_pad, nieuw_pad)
        logger.info(f"Bestand wordt verplaatst naar:\n{nieuw_pad}")

    if actie == "kopieer":
        nieuw_pad = os.path.join(param, nieuwe_naam)
        nieuwe_map = os.path.dirname(nieuw_pad)

        if not os.path.isdir(nieuwe_map):
            logger.info(f"Map wordt aangemaakt:\n{nieuwe_map}")
            os.makedirs(nieuwe_map)

        logger.info(f"Bestand wordt gekopieerd naar:\n{nieuw_pad}")
        shutil.copy2(invoer_pad, nieuw_pad)

    if actie == "hernoem":
        nieuw_pad = os.path.join(
            os.path.dirname(invoer_pad), os.path.basename(nieuwe_naam)
        )

        logger.info(f"Bestand wordt hernoemd naar:\n{nieuw_pad}")
        os.rename(invoer_pad, nieuw_pad)


def main():
    opties = lees_opties()

    eg_log.configureer_log(logger, opties.debug)

    logger.debug(f"Opties:\n{opties}")

    try:
        eg_commando.vereis_programma("tar")
        eg_commando.vereis_programma("sha1sum")
        
        hernoem(opties.invoer, opties)
    except Exception as error:
        eg_log.log_error(logger, error)


if __name__ == "__main__":
    main()
