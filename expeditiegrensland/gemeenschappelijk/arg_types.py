import os
from argparse import ArgumentTypeError
import re


def bestaand_pad(pad: str):
    if not os.path.exists(pad):
        raise ArgumentTypeError(f"'{pad}' bestaat niet")

    return os.path.abspath(pad)


def bestaand_bestand(pad: str):
    if not os.path.isfile(pad):
        raise ArgumentTypeError(f"'{pad}' bestaat niet")

    return os.path.abspath(pad)


def een_map(pad: str):
    if os.path.exists(pad) and not os.path.isdir(pad):
        raise ArgumentTypeError(f"'{pad}' is geen map")

    if not os.path.exists(pad):
        try:
            os.makedirs(pad)
        except:
            raise ArgumentTypeError(f"'{pad}' kon niet worden gemaakt")

    return os.path.abspath(pad)


def lege_map(pad: str):
    de_map = een_map(pad)

    if os.listdir(de_map):
        raise ArgumentTypeError(f"'{pad}' is niet leeg")

    return de_map


def slak(tekst: str):
    m = re.compile("^[a-z-]+$")

    if not m.match(tekst):
        raise ArgumentTypeError("Een slak mag alleen letters en streepjes (-) bevatten")

    return tekst
