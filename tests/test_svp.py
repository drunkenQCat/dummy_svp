import pytest
from pydantic import ValidationError
from models.svp import Svp  # Replace with the correct import path

# Example of the JSON data you provided
svp_data = {
    "version": 153,
    "time": {
        "meter": [{"index": 0, "numerator": 4, "denominator": 4}],
        "tempo": [{"position": 0, "bpm": 120.0}],
    },
    "library": [],
    "tracks": [
        {
            "name": "未命名音轨",
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
                ],
            },
            "mainRef": {
                "groupID": "a591d7ea-0990-4319-bdd9-3d0c7c1774c2",
                "blickAbsoluteBegin": 0,
                "blickAbsoluteEnd": -1,
                "blickOffset": 0,
                "pitchOffset": 0,
                "isInstrumental": False,
                "systemPitchDelta": {
                    "mode": "cubic",
                    "points": [],
                },
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
    ],
    "renderConfig": {
        "destination": "",
        "filename": "未命名",
        "numChannels": 1,
        "aspirationFormat": "noAspiration",
        "bitDepth": 16,
        "sampleRate": 44100,
        "exportMixDown": True,
        "exportPitch": False,
    },
}


# Unit test for the Svp model
def test_svp_model():
    try:
        svp_instance = Svp(**svp_data)
        assert svp_instance.version == 153
        assert svp_instance.time.meter[0].numerator == 4
        assert svp_instance.time.tempo[0].bpm == 120.0
        assert len(svp_instance.tracks) == 1  # Ensure there is 1 track
        assert svp_instance.tracks[0].name == "未命名音轨"
        assert svp_instance.renderConfig.filename == "未命名"
    except ValidationError as e:
        pytest.fail(f"Validation error: {e}")


def test_read_from_file():
    with open("example svp.json", "r") as f:
        json_data = f.read()
        svp_example = Svp.model_validate_json(json_data)
    assert svp_example.time.meter[0].denominator == 4
    assert svp_example.tracks[0].mainRef.systemPitchDelta.extract_points_coordinate()[
        0
    ] == [-134064012, 0.0]
