from models.svp import Svp
from models.word import Word


def generate_words_from_svp(svp: Svp) -> list[Word]:
    takes = svp.tracks[0].mainGroup.notes
    return [Word(svp_note=note) for note in takes]


def update_name_to_doremi(doremi: dict[str, str], words: list[Word]):
    for current_word in words:
        current_pitch = current_word.pitch.name
        current_word.name = doremi[current_pitch]


def update_lyric_to_doremi(words: list[Word]):
    for current_word in words:
        note = current_word.svp_note
        note.lyrics = current_word.name
