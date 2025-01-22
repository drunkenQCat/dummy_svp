from music21.note import Note
from music21.pitch import Pitch
from music21.scale import MajorScale, MinorScale
from music21.stream.base import Part

from models.word import Word


# 创建音符到 do re mi 的映射
def create_do_re_mi_map(
    scale_obj: MajorScale | MinorScale,
) -> dict[str, str]:
    # List of do-re-mi syllables for the natural notes
    do_re_mi_names = ["do", "re", "mi", "fa", "sol", "la", "ti"]
    do_re_mi_map = {}

    # Get all pitches in the scale and their corresponding do-re-mi names
    def map_scale_notes_to_doremi(scale_pitches: list[Pitch]) -> dict[str, str]:
        scale_map = {}
        for i, pitch_obj in enumerate(scale_pitches):
            pitch_midi = pitch_obj.midi
            # confer the name align to music21
            pitch_name = Pitch(pitch_midi).name
            scale_map[pitch_name] = do_re_mi_names[i % 7]
        return scale_map

    # Map the scale notes (major or minor)
    scale_pitches = scale_obj.getPitches()
    do_re_mi_map.update(map_scale_notes_to_doremi(scale_pitches))

    # Map chromatic notes by appending 's' to the previous scale note
    chromatic_scale = ["C", "C#", "D", "E-", "E", "F", "F#", "G", "G#", "A", "B-", "B"]

    def get_chromatic_doremi(chrom_pitch: Pitch):
        base_note = chrom_pitch.name[:-1]  # Remove accidental
        if chrom_pitch.name not in do_re_mi_map:
            # Find the previous scale note and add 's' for sharp
            previous_note = chromatic_scale[chromatic_scale.index(chrom_pitch.name) - 1]
            return do_re_mi_map.get(previous_note, "") + "s"
        return do_re_mi_map[base_note]

    # Map chromatic notes outside the scale
    chromatic_map = {}
    for current_note in chromatic_scale:
        chrom_pitch = Pitch(current_note)
        chrom_pitch_name = chrom_pitch.name
        if chrom_pitch_name not in do_re_mi_map:
            chromatic_map[chrom_pitch_name] = get_chromatic_doremi(chrom_pitch)

    # Update the map with chromatic notes
    do_re_mi_map.update(chromatic_map)

    return do_re_mi_map


# Example Usage with a Major Scale

major_scale = MajorScale("C")
scale_map = create_do_re_mi_map(major_scale)
print(scale_map)
# 分析 MIDI 文件的音符并推测其调式


def analyze_scale(midi_notes: list[int]) -> MajorScale | MinorScale:
    # Create a Part object and add the MIDI notes as notes

    part = Part()
    for midi_value in midi_notes:
        n = Note(midi_value)
        part.append(n)

    # Use the `Key` class to analyze the key of the Part
    key_signature = part.analyze("key")

    # Return the tonic and the mode of the scale
    tonic_name = key_signature.tonic.name
    mode = key_signature.mode

    print(f"The scale is {tonic_name} {mode}")
    return key_signature.getScale()


# 从 MIDI 文件中提取并转换音符为 do re mi
def get_doremi_from_words(words: list[Word]):
    # 解析 MIDI 文件
    midi_notes = [current.svp_note.pitch for current in words]
    analyse = analyze_scale(midi_notes)
    doremi_map = create_do_re_mi_map(analyse)

    return doremi_map
