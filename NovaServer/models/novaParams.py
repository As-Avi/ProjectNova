from pydantic import BaseModel
from typing import List
from typing_extensions import TypedDict

class ParInWithFilter(BaseModel):
    config: str
    language: str
    filter: str

class ParIn(BaseModel):
    config: str
    language: str


class Item(TypedDict):
    id: str
    name: str



class ParOut(BaseModel):
    title: str
    module: str
    findfields: str
    items: List[Item] = []
    
class ComboOut(BaseModel):
    label: str
    values: List[str] = []