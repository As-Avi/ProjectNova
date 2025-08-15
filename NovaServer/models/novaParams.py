from pydantic import BaseModel
from typing import List

class ParInWithFilter(BaseModel):
    config: str
    language: str
    filter:str

class ParIn(BaseModel):
    config: str
    language: str

class ParOut(BaseModel):
    title: str


class ComboOut(BaseModel):
    label: str
    values: List[str] = []