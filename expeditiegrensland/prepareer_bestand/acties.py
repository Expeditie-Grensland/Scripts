from genericpath import exists
from logging import getLogger
from os import path, walk
from shutil import copytree, move

import boto3

logger = getLogger("__main__")


def verplaats_actie_fabriek(uit_map: str):
    def verplaats_actie(in_pad: str, naam: str):
        uit_pad = path.join(uit_map, naam)
        logger.info(f"Verplaatsen naar:\n{uit_pad}")
        if exists(uit_pad):
            raise FileExistsError("Uitvoermap bestaat al")
        move(in_pad, uit_pad)

    return verplaats_actie


def kopieer_actie_fabriek(uit_map: str):
    def kopieer_actie(in_pad: str, naam: str):
        uit_pad = path.join(uit_map, naam)
        logger.info(f"Kopiëren naar:\n{uit_pad}")
        if exists(uit_pad):
            raise FileExistsError("Uitvoermap bestaat al")
        copytree(in_pad, path.join(uit_map, naam))

    return kopieer_actie


def upload_actie_fabriek(uit_map: str):
    emmer, *emmer_pad = uit_map.split("/", 1) + [""]
    emmer_pad = emmer_pad[0]

    def upload_actie(in_pad: str, naam: str):
        sleutel_basis = path.join(emmer_pad, naam).replace(path.sep, "/")
        logger.info(f"Uploaden naar:\nEmmer: {emmer}\nSleutel-basis: {sleutel_basis}/")

        s3_klant = boto3.client("s3")  # type: ignore

        for _, _, bestanden in walk(in_pad, topdown=False):
            for bestand in bestanden:
                pad = path.join(in_pad, bestand)
                sleutel = path.join(emmer_pad, naam, bestand).replace(path.sep, "/")

                logger.debug(
                    f"Uploaden van object:\nBestand: {pad}\nSleutel: {sleutel}"
                )
                s3_klant.upload_file(pad, emmer, sleutel)

    return upload_actie
