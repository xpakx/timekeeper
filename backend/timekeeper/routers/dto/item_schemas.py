from pydantic import BaseModel
from ...db.models import ItemRarity


class ItemBase(BaseModel):
    id: int
    name: str
    rarity: ItemRarity

    class Config:
        orm_mode = True


class EquipmentBase(BaseModel):
    id: int
    amount: int
    item: ItemBase

    class Config:
        orm_mode = True
