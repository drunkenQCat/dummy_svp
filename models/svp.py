from pydantic import BaseModel, Field
from models.svp_track import Track
from typing import List, Self


class Meter(BaseModel):
    index: int
    numerator: int
    denominator: int


class Tempo(BaseModel):
    position: int
    bpm: float


class Time(BaseModel):
    meter: List[Meter] = Field(default_factory=list)
    tempo: List[Tempo] = Field(default_factory=list)


class RenderConfig(BaseModel):
    """
    {
        "destination": "",
        "filename": "\u672a\u547d\u540d",
        "numChannels": 1,
        "aspirationFormat": "noAspiration",
        "bitDepth": 16,
        "sampleRate": 44100,
        "exportMixDown": true,
        "exportPitch": false
    }
    """

    destination: str = ""
    filename: str = "未命名"  # 未命名
    numChannels: int = 1
    aspirationFormat: str = "noAspiration"
    bitDepth: int = 16
    sampleRate: int = 44100
    exportMixDown: bool = True
    exportPitch: bool = False

    @classmethod
    def from_filename(cls, filename: str) -> Self:
        """
        Initializes the RenderConfig instance with the given filename.
        Other parameters are set to default values as described in the docstring.
        """
        return cls(filename=filename)


class Svp(BaseModel):
    version: int = 153
    time: Time
    library: list = Field(default_factory=list)
    tracks: list[Track] = Field(default_factory=list)
    renderConfig: RenderConfig
