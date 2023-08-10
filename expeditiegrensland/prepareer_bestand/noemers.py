def dynamische_slak(slak: str):
    return "{naam}" if slak == "-" else slak


def film_noemer_fabiek(slak: str):
    return f"{dynamische_slak(slak)}/film.{{hash}}/"


def achtergrond_noemer_fabriek(slak: str):
    return f"{dynamische_slak(slak)}/film.{{hash}}.jpg"


def woord_afbeelding_noemer_fabriek(slak: str):
    return f"woordenboek/{dynamische_slak(slak)}.{{hash}}.jpg"


def woord_video_noemer_fabriek(slak: str):
    return f"woordenboek/{dynamische_slak(slak)}.{{hash}}.mp4"


def woord_audio_noemer_fabriek(slak: str):
    return f"woordenboek/{dynamische_slak(slak)}.{{hash}}.aac"


def citaat_afbeelding_noemer_fabriek(slak: str):
    return f"citaten/{dynamische_slak(slak)}.{{hash}}.jpg"


def citaat_video_noemer_fabriek(slak: str):
    return f"citaten/{dynamische_slak(slak)}.{{hash}}.mp4"


def citaat_audio_noemer_fabriek(slak: str):
    return f"citaten/{dynamische_slak(slak)}.{{hash}}.aac"


def verhaal_afbeelding_noemer_fabriek(slak: str):
    return f"{dynamische_slak(slak)}/verhaal.{{hash}}.jpg"


def verhaal_video_noemer_fabriek(slak: str):
    return f"{dynamische_slak(slak)}/verhaal.{{hash}}.mp4"


def verhaal_audio_noemer_fabriek(slak: str):
    return f"{dynamische_slak(slak)}/verhaal.{{hash}}.aac"
