import os
import argparse


def bestaand_pad(pad):
    if not os.path.exists(pad):
        raise argparse.ArgumentTypeError(f"'{pad}' bestaat niet")

    return os.path.abspath(pad)


def bestaand_bestand(pad):
    if not os.path.isfile(pad):
        raise argparse.ArgumentTypeError(f"'{pad}' bestaat niet")

    return os.path.abspath(pad)


def een_map(pad):
    if os.path.exists(pad) and not os.path.isdir(pad):
        raise argparse.ArgumentTypeError(f"'{pad}' is geen map")

    if not os.path.exists(pad):
        try:
            os.makedirs(pad)
        except:
            raise argparse.ArgumentTypeError(f"'{pad}' kon niet worden gemaakt")
        
    return os.path.abspath(pad)


def lege_map(pad):
    de_map = een_map(pad)

    if os.listdir(de_map):
        raise argparse.ArgumentTypeError(f"'{pad}' is niet leeg")
    
    return de_map
