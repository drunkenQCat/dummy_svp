from pydantic import BaseModel, Field, model_validator
from typing import List, Dict, Literal, Self
from uuid import UUID


# 定义子模型：Mixer
class Mixer(BaseModel):
    gainDecibel: float
    pan: float
    mute: bool
    solo: bool
    display: bool


class Take(BaseModel):
    id: int
    expr: float
    liked: bool = False


class TakeList(BaseModel):
    activeTakeId: int
    takes: List[Take] = Field(default_factory=list)


class SystemAttributes(BaseModel):
    tF0Offset: float = -0.0
    tF0Left: float = 0.1000000014901161
    tF0Right: float = 0.1000000014901161
    dF0Left: float = 0.0
    dF0Right: float = 0.0
    dF0Vbr: float = 0.0
    evenSyllableDuration: bool = True


# Example usage
example_system_attributes = SystemAttributes()
print(example_system_attributes)


# 定义子模型：Note
class Note(BaseModel):
    musicalType: Literal["singing", "rapping"] = "singing"
    onset: int = 0
    duration: int
    lyrics: str
    phonemes: str
    accent: str
    pitch: int
    detune: float
    instantMode: bool
    attributes: Dict[str, bool]
    systemAttributes: SystemAttributes
    pitchTakes: TakeList
    timbreTakes: TakeList


class Parameter(BaseModel):
    mode: Literal["cubic", "linear", "cosine"] = "cubic"
    points: List[int | float] = Field(default_factory=list)

    def extract_points_coordinate(self):
        # 反转展平的列表为二维列表
        grouped = [self.points[i : i + 2] for i in range(0, len(self.points), 2)]
        return grouped

    @model_validator(mode="after")
    def check_points_coordinate(self) -> Self:
        coordinates = self.extract_points_coordinate()
        if len(coordinates) == 0:
            return self
        for point in coordinates:
            if isinstance(point[0], int) and isinstance(point[1], float):
                continue
            raise ValueError("Illegal point detected")
        return self


# 定义子模型：MainGroup
class MainGroup(BaseModel):
    name: str
    uuid: UUID
    parameters: Dict[str, Parameter]
    vocalModes: Dict[str, object]  # This could be customized if we know the structure
    notes: List[Note]


# 定义子模型：Voice
class Voice(BaseModel):
    vocalModeInherited: bool
    vocalModePreset: str
    vocalModeParams: Dict[str, object]


# 定义子模型：Database
class Database(BaseModel):
    name: str
    language: str
    phoneset: str
    languageOverride: str
    phonesetOverride: str
    backendType: str
    version: str


# 定义子模型：MainRef
class MainRef(BaseModel):
    groupID: UUID
    blickAbsoluteBegin: int
    blickAbsoluteEnd: int
    blickOffset: int
    pitchOffset: int
    isInstrumental: bool
    systemPitchDelta: Parameter
    database: Database
    dictionary: str
    voice: Voice
    pitchTakes: TakeList
    timbreTakes: TakeList


# 定义子模型：Track
class Track(BaseModel):
    name: str
    dispColor: str = "ff7db235"
    dispOrder: int = 0
    renderEnabled: bool = False
    mixer: Mixer
    mainGroup: MainGroup
    mainRef: MainRef
    groups: List = Field(default_factory=list)


# 定义主模型：TracksContainer
class TracksContainer(BaseModel):
    tracks: List[Track]


# 示例：使用示例数据创建一个 TracksContainer 对象
data = {
    "tracks": [
        {
            "name": "\u672a\u547d\u540d\u97f68音轨",
            "dispColor": "ff7db235",
            "dispOrder": 0,
            "renderEnabled": False,
            "mixer": {
                "gainDecibel": 0.0,
                "pan": 0.0,
                "mute": False,
                "solo": False,
                "display": True,
            },
            "mainGroup": {
                "name": "main",
                "uuid": "a591d7ea-0990-4319-bdd9-3d0c7c1774c2",
                "parameters": {
                    "pitchDelta": {"mode": "cubic", "points": []},
                    "vibratoEnv": {
                        "mode": "cubic",
                        "points": [2296938098, 0.199999988079071],
                    },
                    "loudness": {"mode": "cubic", "points": []},
                    "tension": {"mode": "cubic", "points": [2239089333, 0.0]},
                    "breathiness": {"mode": "cubic", "points": []},
                    "voicing": {"mode": "cubic", "points": []},
                    "gender": {"mode": "cubic", "points": []},
                    "toneShift": {"mode": "cubic", "points": []},
                },
                "vocalModes": {},
                "notes": [
                    {
                        "musicalType": "singing",
                        "onset": 0,
                        "duration": 705600000,
                        "lyrics": "do",
                        "phonemes": "",
                        "accent": "",
                        "pitch": 60,
                        "detune": 0,
                        "instantMode": True,
                        "attributes": {"evenSyllableDuration": True},
                        "systemAttributes": {
                            "tF0Offset": -0.0,
                            "tF0Left": 0.1000000014901161,
                            "tF0Right": 0.1000000014901161,
                            "dF0Left": 0.0,
                            "dF0Right": 0.0,
                            "dF0Vbr": 0.0,
                            "evenSyllableDuration": True,
                        },
                        "pitchTakes": {
                            "activeTakeId": 0,
                            "takes": [{"id": 0, "expr": 0.0, "liked": False}],
                        },
                        "timbreTakes": {
                            "activeTakeId": 0,
                            "takes": [{"id": 0, "expr": 0.0, "liked": False}],
                        },
                    }
                    # 其他 Notes 按照相同格式继续
                ],
            },
            "mainRef": {
                "groupID": "a591d7ea-0990-4319-bdd9-3d0c7c1774c2",
                "blickAbsoluteBegin": 0,
                "blickAbsoluteEnd": -1,
                "blickOffset": 0,
                "pitchOffset": 0,
                "isInstrumental": False,
                "systemPitchDelta": {"mode": "cubic", "points": []},
                "database": {
                    "name": "D-Lin (FLT)",
                    "language": "mandarin",
                    "phoneset": "xsampa",
                    "languageOverride": "english",
                    "phonesetOverride": "arpabet",
                    "backendType": "SVR2AI",
                    "version": "100",
                },
                "dictionary": "",
                "voice": {
                    "vocalModeInherited": True,
                    "vocalModePreset": "",
                    "vocalModeParams": {},
                },
                "pitchTakes": {
                    "activeTakeId": 0,
                    "takes": [{"id": 0, "expr": 0.0, "liked": False}],
                },
                "timbreTakes": {
                    "activeTakeId": 0,
                    "takes": [{"id": 0, "expr": 0.0, "liked": False}],
                },
            },
            "groups": [],
        }
    ]
}
