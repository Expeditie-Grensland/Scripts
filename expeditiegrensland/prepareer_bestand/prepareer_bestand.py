from dataclasses import dataclass

from .converteerders.basis import Converteerder
from .noemers.basis import Noemer


@dataclass
class PrepareerBestandOpties:
    converteerder: Converteerder
    noemer: Noemer
