from os import makedirs, path
from ..gemeenschappelijk.commando import draai, vereis_programma


def film_converteerder_fabriek():
    vereis_programma("ffmpeg")

    def film_converteerder(in_pad: str, uit_map: str):
        pass

    return film_converteerder


def _converteer_afbeelding(in_pad: str, uit_pad: str, breedte: int):
    draai(
        [
            "gm",
            "convert",
            in_pad,
            "-colorspace",
            "RGB",
            "-sampling-factor",
            "4:2:0",
            "-define",
            "jpeg:dct-method=float",
            "-quality",
            "80",
            "-interlace",
            "Plane",
            "-strip",
            "-resize",
            str(breedte),
            uit_pad,
        ]
    )


def achtergrond_converteerder_fabriek():
    vereis_programma("gm", "GraphicsMagick")

    def achtergrond_converteerder(in_pad: str, uit_map: str):
        _converteer_afbeelding(in_pad, path.join(uit_map, "achtergrond.jpg"), 1500)
        _converteer_afbeelding(in_pad, path.join(uit_map, "achtergrond-klein.jpg"), 500)
        _converteer_afbeelding(in_pad, path.join(uit_map, "achtergrond-minuscuul.jpg"), 16)

    return achtergrond_converteerder


def afbeelding_bijlage_converteerder_fabriek():
    vereis_programma("convert")

    def afbeelding_bijlage_converteerder(in_pad: str, uit_map: str):
        pass

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
