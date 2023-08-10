from dataclasses import dataclass


@dataclass
class Video2DashConfigVideo:
    codec: str
    profiel: str
    bitsnelheid: int
    breedte: int
    hoogte: int
    beeldsnelheid: int


@dataclass
class Video2DashConfigAudio:
    codec: str
    profiel: str
    bitsnelheid: int


@dataclass
class Video2DashConfigTerugval:
    naam: str
    video: Video2DashConfigVideo
    audio: Video2DashConfigAudio


@dataclass
class Video2DashConfig:
    snelheid: str
    dash_videos: list[Video2DashConfigVideo]
    dash_audios: list[Video2DashConfigAudio]
    terugval: list[Video2DashConfigTerugval]
