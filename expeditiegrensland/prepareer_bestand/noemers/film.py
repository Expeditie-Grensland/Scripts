from .basis import Noemer


class FilmNoemer(Noemer):
    expeditie: str

    def __init__(self, expeditie: str):
        self.expeditie = expeditie

    def noem(self, inputnaam: str) -> str:
        return super().noem(inputnaam)
