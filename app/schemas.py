from pydantic import BaseModel

class NoteCreate(BaseModel):
    title: str
    content: str

class NoteResponse(NoteCreate):
    id: int
    class config:
        from_attributes = True