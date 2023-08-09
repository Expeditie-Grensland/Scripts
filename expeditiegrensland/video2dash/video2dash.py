"""Zet een videobestand om naar dash bestanden voor gebruik op de website"""

import logging
import os
from abc import ABC, abstractmethod
from dataclasses import dataclass
from functools import cached_property

from dataclass_wizard import YAMLWizard

from ..gemeenschappelijk.commando import draai

logger = logging.getLogger("__main__")


@dataclass
class ConfigVideo:
    codec: str
    profiel: str
    bitsnelheid: int
    breedte: int
    hoogte: int
    beeldsnelheid: int


@dataclass
class ConfigAudio:
    codec: str
    profiel: str
    bitsnelheid: int


@dataclass
class ConfigTerugval:
    naam: str
    video: ConfigVideo
    audio: ConfigAudio


@dataclass
class Config(YAMLWizard):
    snelheid: str
    dash_videos: list[ConfigVideo]
    dash_audios: list[ConfigAudio]
    terugval: list[ConfigTerugval]


class ConfigBestand(ABC):
    @abstractmethod
    def krijg_pad(self) -> str:
        raise NotImplementedError()

    @cached_property
    def config(self) -> Config:
        pad = self.krijg_pad()
        logger.info(f"Configuratie wordt gelezen uit: '{pad}'")
        config = Config.from_yaml_file(self.krijg_pad())
        logger.debug(f"Configuratie:\n{config}")
        return config


class ConfigBestandIngebouwd(ConfigBestand):
    naam: str

    def __init__(self, naam: str):
        self.naam = naam

    def krijg_pad(self) -> str:
        return os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            f"configs/{self.naam}.yml",
        )


class ConfigBestandExtern(ConfigBestand):
    pad: str

    def __init__(self, pad: str):
        self.pad = pad

    def krijg_pad(self) -> str:
        return self.pad


@dataclass
class Video2DashOpties:
    invoer: str
    uitvoer: str
    max_resolutie: int
    beeldsnelheid: int
    config_bestand: ConfigBestand
    debug: bool


def video2dash(opties: Video2DashOpties):
    config = opties.config_bestand.config

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

        draai(opdracht)
