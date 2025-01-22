from music21 import converter


def get_midi_key(path):
    score = converter.parse(path)
    key = score.analyze("key")
    key.getScales()
    print(key.tonic.name, key.mode)  # pyright: ignore


def analyze_key_from_notes(notes):
    # 获取音符的所有名称
    pitches = [n.name for n in notes if isinstance(n, note.Note)]

    # 通过音符分析推测调式
    key_analysis = key.KeySignature()
    key_analysis = key_analysis.analyze(pitches)

    return key_analysis
