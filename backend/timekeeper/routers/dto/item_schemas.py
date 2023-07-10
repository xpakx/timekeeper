from pydantic import BaseModel
from ...db.models import ItemRarity


class ItemBase(BaseModel):
    id: int
    name: str
    rarity: ItemRarity

    class Config:
        orm_mode = True
