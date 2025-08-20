from pydantic import BaseModel
from typing import List


class ParInWithFilter(BaseModel):
    config: str
    language: str
    filter: str

from typing_extensions import TypedDict
class ParIn(BaseModel):
    config: str
    language: str


class Item(TypedDict):
    id: str
    name: str

class ItemList(BaseModel):
    items: List[Item]

class ParOut(BaseModel):
    title: str
    module: str
    findfields: str
    items: list[Item] = []
    


class ComboOut(BaseModel):
    label: str
    values: List[str] = []