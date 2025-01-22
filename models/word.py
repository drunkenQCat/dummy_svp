from models.svp_track import Note
from music21.pitch import Pitch
from pydantic import BaseModel


class Word(BaseModel):
    svp_note: Note
    name: str = ""

    @property
    def pitch(self) -> Pitch:
        return Pitch(self.svp_note.pitch)
