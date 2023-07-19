#!/usr/bin/env python3

import os
import argparse


def bestaand_bestand(pad):
    if not os.path.isfile(pad):
        raise argparse.ArgumentTypeError(f"'{pad}' bestaat niet")

    return os.path.abspath(pad)


def lege_map(pad):
    if os.path.exists(pad) and not os.path.isdir(pad):
        raise argparse.ArgumentTypeError(f"'{pad}' is geen map")

    if os.path.isdir(pad) and os.listdir(pad):
        raise argparse.ArgumentTypeError(f"'{pad}' is niet leeg")

    if not os.path.exists(pad):
        try:
            os.makedirs(pad)
        except:
            raise argparse.ArgumentTypeError(f"'{pad}' kon niet worden gemaakt")

    return os.path.abspath(pad)
