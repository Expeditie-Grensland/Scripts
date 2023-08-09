from abc import ABC, abstractmethod


class Converteerder(ABC):
    @abstractmethod
    def converteer(self):
        pass
