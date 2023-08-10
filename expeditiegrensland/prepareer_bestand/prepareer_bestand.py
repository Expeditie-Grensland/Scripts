from logging import getLogger
from os import path
from tempfile import TemporaryDirectory
from typing import Callable

from ..gemeenschappelijk.commando import draai_pijp

logger = getLogger("__main__")


def bepaal_bestandsnaam(in_pad: str, tmp_pad: str, noemer: str):
    in_naam = path.splitext(path.basename(in_pad))[0]

    if path.isdir(tmp_pad) and noemer.endswith("/"):
        assert path.isdir(tmp_pad)
        hash_commando = [
            ["tar", "-c", "-f", "-", "-C", tmp_pad, "--sort=name", "."],
            ["sha1sum"],
        ]
    elif path.isfile(tmp_pad) and not noemer.endswith("/"):
        assert path.isfile(tmp_pad)
        hash_commando = [["sha1sum", tmp_pad]]
    else:
        raise RuntimeError("Bestand is niet juist geconverteerd")

    hash = draai_pijp(hash_commando).split(" ")[0][:8]

    return noemer.format(naam=in_naam, hash=hash)


def prepareer_bestand(
    invoer: list[str], converteerder: Callable[[str], str], noemer: str
):
    for in_pad in invoer:
        with TemporaryDirectory() as tmp_map:
            logger.info(f"Invoer bestand:\n{in_pad}")

            logger.debug(f"Tijdelijke map:\n{tmp_map}")

            tmp_pad = converteerder(tmp_map)
            logger.info(f"Tijdelijk pad van geconverteerd bestand:\n{tmp_pad}")

            naam = bepaal_bestandsnaam(in_pad, tmp_pad, noemer)
            logger.info(f"Nieuwe naam:\n{naam}")
