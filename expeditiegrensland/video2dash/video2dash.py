#!/usr/bin/env python3

"""Zet een videobestand om naar dash bestanden voor gebruik op de website"""

import argparse
import logging
import os
import subprocess
import sys
from dataclasses import dataclass

from dataclass_wizard import YAMLWizard

import expeditiegrensland.gemeenschappelijk.arg_types as eg_arg_types
import expeditiegrensland.gemeenschappelijk.log as eg_log
import expeditiegrensland.gemeenschappelijk.commando as eg_commando

logger = logging.getLogger("eg-video2dash")


def lees_opties():
    parser = argparse.ArgumentParser(
        prog="eg-video2dash",
        description=sys.modules[__name__].__doc__,
        allow_abbrev=False,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    config = parser.add_mutually_exclusive_group()

    config.set_defaults(config="film")

    config.add_argument(
        "--film",
        dest="config",
        action="store_const",
        const="film",
        help="Gebruik configuratiebestand voor films (standaard)",
    )

    config.add_argument(
        "--config",
        dest="config_bestand",
        type=eg_arg_types.bestaand_bestand,
        help="Gebruik een ander configuratiebestand",
        metavar="BESTAND",
    )

    parser.add_argument(
        "--max-resolutie",
        type=int,
        default=1080,
        help="Maximale resolutie (in verticale pixels) om bestanden in te produceren (standaard: %(default)s)",
        metavar="HOOGTE",
    )

    parser.add_argument(
        "--beeldsnelheid",
        type=int,
        default=60,
        help="Beeldsnelheid van het invoer videobestand (standaard: %(default)s)",
        metavar="BPS",
    )

    parser.add_argument(
        "--debug",
        action="store_true",
        help="Schrijf foutopsporingsinformatie naar de terminal",
    )

    parser.add_argument(
        "invoer",
        type=eg_arg_types.bestaand_bestand,
        help="Videobestand dat omgezet dient te worden",
    )

    parser.add_argument(
        "uitvoer",
        type=eg_arg_types.lege_map,
        help="Map om omgezette bestanden in op te slaan (dient leeg of afwezig te zijn)",
    )

    return parser.parse_args()


@dataclass
class ConfigBestandVideo:
    codec: str
    profiel: str
    bitsnelheid: int
    breedte: int
    hoogte: int
    beeldsnelheid: int


@dataclass
class ConfigBestandAudio:
    codec: str
    profiel: str
    bitsnelheid: int


@dataclass
class ConfigBestandTerugval:
    naam: str
    video: ConfigBestandVideo
    audio: ConfigBestandAudio


@dataclass
class ConfigBestand(YAMLWizard):
    snelheid: str
    dash_videos: list[ConfigBestandVideo]
    dash_audios: list[ConfigBestandAudio]
    terugval: list[ConfigBestandTerugval]


def lees_config(opties):
    if not opties.config_bestand:
        opties.config_bestand = os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            f"configs/{opties.config}.yml",
        )

    logger.info(f"Configuratie wordt gelezen uit: '{opties.config_bestand}'")
    config = ConfigBestand.from_yaml_file(opties.config_bestand)
    logger.debug(f"Configuratie:\n{config}")

    return config


def zet_om(opties, config: ConfigBestand):
    os.chdir(opties.uitvoer)

    opdracht = ["ffmpeg", "-hide_banner"]

    if not opties.debug:
        opdracht += [
            "-loglevel",
            "warning",
        ]

    opdracht += [
        "-i",
        opties.invoer,
        "-preset",
        config.snelheid,
        "-f",
        "dash",
        "-use_template",
        "1",
        "-use_timeline",
        "1",
        "-seg_duration",
        "2",
        "-init_seg_name",
        "stream-$RepresentationID$/init.$ext$",
        "-media_seg_name",
        "stream-$RepresentationID$/chunk-$Number%05d$.$ext$",
        "-adaptation_sets",
        "id=0,streams=v id=1,streams=a",
        "-hls_playlist",
        "1",
        "-hls_master_name",
        "hls.m3u8",
    ]

    logger.debug(f"Basis opdracht:\n{opdracht}")

    stream_id = 0

    i = 0
    for video in config.dash_videos:
        if (
            video.beeldsnelheid > opties.beeldsnelheid
            or video.hoogte > opties.max_resolutie
        ):
            continue

        os.mkdir(f"stream-{stream_id}")
        stream_id += 1

        video_opdracht = [
            "-map",
            "0:v:0",
            f"-c:v:{i}",
            video.codec,
            f"-profile:v:{i}",
            video.profiel,
            f"-b:v:{i}",
            f"{video.bitsnelheid}k",
            f"-maxrate:v:{i}",
            f"{video.bitsnelheid}k",
            f"-bufsize:v:{i}",
            f"{video.bitsnelheid * 1.5}k",
            f"-filter:v:{i}",
            f"scale={video.breedte}:{video.hoogte},format=yuv420p",
            f"-r:v:{i}",
            f"{video.beeldsnelheid or opties.beeldsnelheid}",
            f"-g:v:{i}",
            f"{(video.beeldsnelheid or opties.beeldsnelheid) * 2}",
            f"-keyint_min:v:{i}",
            f"{(video.beeldsnelheid or opties.beeldsnelheid)}",
        ]

        opdracht += video_opdracht
        logger.debug(
            f"Opdracht generatie (dash video stream {i}):\n{video}\n{video_opdracht}"
        )

        i += 1

    for i, audio in enumerate(config.dash_audios):
        os.mkdir(f"stream-{stream_id}")
        stream_id += 1

        audio_opdracht = [
            "-map",
            "0:a:0",
            f"-c:a:{i}",
            audio.codec,
            f"-profile:a:{i}",
            audio.profiel,
            f"-b:a:{i}",
            f"{audio.bitsnelheid}k",
        ]

        opdracht += audio_opdracht
        logger.debug(
            f"Opdracht generatie (dash audio stream {i}):\n{audio}\n{audio_opdracht}"
        )

    opdracht += ["dash.mpd"]

    for terugval in config.terugval:
        video, audio = terugval.video, terugval.audio

        if (
            video.beeldsnelheid > opties.beeldsnelheid
            or video.hoogte > opties.max_resolutie
        ):
            continue

        opdracht += ["-f", "mp4"]

        video_opdracht = [
            "-map",
            "0:v:0",
            "-c:v:0",
            video.codec,
            "-profile:v:0",
            video.profiel,
            "-b:v:0",
            f"{video.bitsnelheid}k",
            "-maxrate:v:0",
            f"{video.bitsnelheid}k",
            "-bufsize:v:0",
            f"{video.bitsnelheid * 1.5}k",
            "-filter:v:0",
            f"scale={video.breedte}:{video.hoogte},format=yuv420p",
            "-r:v:0",
            f"{video.beeldsnelheid or opties.beeldsnelheid}",
        ]

        opdracht += video_opdracht
        logger.debug(
            f"Opdracht generatie (terugval video '{terugval.naam}'):\n{video}\n{video_opdracht}"
        )

        audio_opdracht = [
            "-map",
            "0:a:0",
            "-c:a:0",
            audio.codec,
            "-profile:a:0",
            audio.profiel,
            "-b:a:0",
            f"{audio.bitsnelheid}k",
        ]

        opdracht += audio_opdracht
        logger.debug(
            f"Opdracht generatie (terugval audio '{terugval.naam}'):\n{audio}\n{audio_opdracht}"
        )

        opdracht += ["-movflags", "+faststart", terugval.naam]

        logger.info("FFmpeg wordt gedraaid")

        eg_commando.draai(opdracht, logger)


def main():
    opties = lees_opties()

    eg_log.configureer_log(logger, opties.debug)

    logger.debug(f"Opties:\n{opties}")

    try:
        config = lees_config(opties)

        zet_om(opties, config)
    except Exception as error:
        eg_log.log_error(logger, error)


if __name__ == "__main__":
    main()
