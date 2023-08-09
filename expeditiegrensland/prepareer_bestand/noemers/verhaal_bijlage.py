from .basis import Noemer


class VerhaalBijlageNoemer(Noemer):
    slak: str

    def __init__(self, slak: str):
        self.slak = slak
