from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from os import path

from ..gemeenschappelijk.commando import draai, vereis_programma


@dataclass
class AfbeeldingVersie(ABC):
    naam: str
    opties: list[str] = field(default_factory=list)

    @abstractmethod
    def krijg_opties(self) -> list[str]:
        raise NotImplementedError


@dataclass
class JpegAfbeeldingVersie(AfbeeldingVersie):
    def __post_init__(self):
        self.naam = self.naam + ".jpg"

    def krijg_opties(self):
        return [
            "-colorspace",
            "sRGB",
            "-sampling-factor",
            "4:2:0",
            "-quality",
            "80",
            "-strip",
            *self.opties,
        ]


@dataclass
class WebpAfbeeldingVersie(AfbeeldingVersie):
    def __post_init__(self):
        self.naam = self.naam + ".webp"

    def krijg_opties(self):
        return ["-colorspace", "sRGB", "-quality", "80", "-strip", *self.opties]


def film_converteerder_fabriek():
    vereis_programma("ffmpeg")

    def film_converteerder(in_pad: str, uit_map: str):
        pass

    return film_converteerder


def _converteer_afbeeldingen(
    in_pad: str, uit_map: str, versies: list[AfbeeldingVersie]
):
    for versie in versies:
        draai(
            [
                "magick",
                in_pad,
                *versie.krijg_opties(),
                path.join(uit_map, versie.naam),
            ]
        )


def achtergrond_converteerder_fabriek():
    vereis_programma("magick", "ImageMagick 7+")

    def achtergrond_converteerder(in_pad: str, uit_map: str):
        _converteer_afbeeldingen(
            in_pad,
            uit_map,
            [
                JpegAfbeeldingVersie("normaal", ["-thumbnail", "1500>"]),
                WebpAfbeeldingVersie("normaal", ["-thumbnail", "1500>"]),
                JpegAfbeeldingVersie("klein", ["-thumbnail", "500>"]),
                WebpAfbeeldingVersie("klein", ["-thumbnail", "500>"]),
                JpegAfbeeldingVersie("miniscuul", ["-thumbnail", "30"]),
            ],
        )

    return achtergrond_converteerder


def afbeelding_bijlage_converteerder_fabriek():
    vereis_programma("magick", "ImageMagick 7+")

    def afbeelding_bijlage_converteerder(in_pad: str, uit_map: str):
        _converteer_afbeeldingen(
            in_pad,
            uit_map,
            [
                JpegAfbeeldingVersie("normaal", ["-thumbnail", "1500>"]),
                WebpAfbeeldingVersie("normaal", ["-thumbnail", "1500>"]),
                JpegAfbeeldingVersie("miniscuul", ["-thumbnail", "30"]),
            ],
        )

    return afbeelding_bijlage_converteerder


def video_bijlage_converteerder_fabriek():
    vereis_programma("ffmpeg")

    def video_bijlage_converteerder(in_pad: str, uit_map: str):
        pass

    return video_bijlage_converteerder


def audio_bijlage_converteerder_fabriek():
    vereis_programma("ffmpeg")

    def audio_bijlage_converteerder(in_pad: str, uit_map: str):
        pass

    return audio_bijlage_converteerder
