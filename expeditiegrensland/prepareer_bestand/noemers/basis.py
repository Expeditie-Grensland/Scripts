from abc import ABC, abstractmethod


class Noemer(ABC):
    @abstractmethod
    def noem(self, inputnaam: str) -> str:
        raise NotImplementedError()
