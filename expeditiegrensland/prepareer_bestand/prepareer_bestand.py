from logging import getLogger
from os import makedirs, path
from tempfile import TemporaryDirectory
from typing import Callable
from uuid import uuid4

from ..gemeenschappelijk.hash import map_hash

logger = getLogger("__main__")


def prepareer_bestand(
    invoer: list[str],
    converteerder: Callable[[str, str], None],
    noemer: str,
    actie: Callable[[str, str], None],
):
    with TemporaryDirectory(prefix="exgrl-") as tmp_map:
        logger.debug(f"Tijdelijke map:\n{tmp_map}")

        for in_pad in invoer:
            logger.info(f"Invoer bestand:\n{in_pad}")

            sub_tmp_map = path.join(tmp_map, str(uuid4()))
            makedirs(sub_tmp_map)
            logger.debug(f"Tijdelijke sub-map:\n{tmp_map}")

            converteerder(in_pad, sub_tmp_map)

            naam = noemer.format(
                naam=path.splitext(path.basename(in_pad))[0],
                hash=map_hash(sub_tmp_map)[:8],
            )
            logger.debug(f"Nieuwe naam:\n{naam}")

            actie(sub_tmp_map, naam)
