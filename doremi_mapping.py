from music21 import converter, note
from music21.stream.base import Score

from utils.midi.key_handler import analyze_key_from_notes


# 创建音符到 do re mi 的映射
def create_do_re_mi_map(scale_obj):
    do_re_mi_names = ["do", "re", "mi", "fa", "sol", "la", "ti"]
    do_re_mi_map = {}

    for i, pitch in enumerate(scale_obj.getPitches()):
        do_re_mi_map[pitch.name] = do_re_mi_names[i % 7]

    return do_re_mi_map


# 分析 MIDI 文件的音符并推测其调式


# 从 MIDI 文件中提取并转换音符为 do re mi
def midi_to_do_re_mi_from_file(midi_file_path):
    # 解析 MIDI 文件
    midi_stream = converter.parse(midi_file_path)

    # 提取音符
    if isinstance(midi_stream, Score):
        notes = midi_stream.parts[0].notes
    else:
        notes = midi_stream.flat.notes

    # 分析调式
    key_analysis = analyze_key_from_notes(notes)
    print(f"推测的调式：{key_analysis.mode} {key_analysis.tonic.name} 大调")

    # 创建 do re mi 映射
    do_re_mi_map = create_do_re_mi_map(key_analysis.getScale())

    # 将音符转换为 do re mi
    do_re_mi_notes = []
    for n in notes:
        if isinstance(n, note.Note):
            pitch_name = n.name
            do_re_mi_notes.append(
                do_re_mi_map.get(pitch_name, pitch_name)
            )  # 如果没有匹配的音符名，返回原音符

    return do_re_mi_notes


# 执行示例
def process_midi_file(midi_file_path):
    do_re_mi_notes = midi_to_do_re_mi_from_file(midi_file_path)
    print(f"转换后的音符（do re mi）: {do_re_mi_notes}")


# 运行示例，替换为你的 MIDI 文件路径
midi_file_path = "path_to_your_midi_file.mid"  # 替换为你的 MIDI 文件路径
process_midi_file(midi_file_path)
