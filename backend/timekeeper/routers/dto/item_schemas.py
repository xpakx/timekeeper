from pydantic import BaseModel
from ...db.models import ItemRarity, ItemType


class ItemBase(BaseModel):
    id: int
    name: str
    num: int
    rarity: ItemRarity
    item_type: ItemType

    class Config:
        orm_mode = True


class EquipmentBase(BaseModel):
    id: int
    amount: int
    item: ItemBase

    class Config:
        orm_mode = True
