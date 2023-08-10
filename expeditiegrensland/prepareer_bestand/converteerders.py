from ..gemeenschappelijk.commando import vereis_programma


def film_converteerder_fabriek():
    vereis_programma("ffmpeg")
    
    def film_converteerder(tmp_map: str):
        return "/home/martijn/Test"

    return film_converteerder


def achtergrond_converteerder_fabriek():
    vereis_programma("convert")

    def achtergrond_converteerder(tmp_map: str):
        return "/home/martijn/Test"

    return achtergrond_converteerder


def afbeelding_bijlage_converteerder_fabriek():
    vereis_programma("convert")

    def afbeelding_bijlage_converteerder(tmp_map: str):
        return "/home/martijn/Test"

    return afbeelding_bijlage_converteerder


def video_bijlage_converteerder_fabriek():
    vereis_programma("ffmpeg")

    def video_bijlage_converteerder(tmp_map: str):
        return "/home/martijn/Test"

    return video_bijlage_converteerder


def audio_bijlage_converteerder_fabriek():
    vereis_programma("ffmpeg")

    def audio_bijlage_converteerder(tmp_map: str):
        return "/home/martijn/Test"

    return audio_bijlage_converteerder
