from pydantic import BaseModel

class ParIn(BaseModel):
    config: str
    language: str

class ParOut(BaseModel):
    title: str
