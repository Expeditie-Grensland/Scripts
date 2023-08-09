from .basis import Noemer


class AchtergrondNoemer(Noemer):
    expeditie: str

    def __init__(self, expeditie: str):
        self.expeditie = expeditie

    def noem(self, inputnaam: str):
        return super().noem(inputnaam)
