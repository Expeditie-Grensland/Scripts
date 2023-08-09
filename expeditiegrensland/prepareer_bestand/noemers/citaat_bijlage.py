from .basis import Noemer


class CitaatBijlageNoemer(Noemer):
    slak: str

    def __init__(self, slak: str):
        self.slak = slak

    def noem(self, inputnaam: str) -> str:
        return super().noem(inputnaam)
