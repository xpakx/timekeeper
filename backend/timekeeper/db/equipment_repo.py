from .models import EquipmentEntry, Item
from sqlalchemy.orm import Session
from sqlalchemy import and_

CRYSTAL = 6


def create_entry(item_id, amount, user_id, db: Session):
    entry_db = db\
        .query(EquipmentEntry)\
        .where(
             and_(
                 EquipmentEntry.owner_id == user_id,
                 EquipmentEntry.item_id == item_id)
            ) .first()
    if entry_db:
        entry_db.amount = entry_db.amount + 1
    else:
        entry = EquipmentEntry(
                item_id=item_id,
                amount=amount,
                owner_id=user_id
                )
        db.add(entry)


def get_items(page: int, size: int, user_id: int, db: Session):
    offset = page*size
    return db\
        .query(EquipmentEntry)\
        .where(
                    and_(EquipmentEntry.owner_id == user_id,
                         EquipmentEntry.amount > 0)
                    )\
        .offset(offset)\
        .limit(size)\
        .all()


def subtract_items(item_id, amount, user_id, db: Session):
    entry = db\
        .query(EquipmentEntry)\
        .join(Item, EquipmentEntry.item)\
        .where(
             and_(
                 EquipmentEntry.owner_id == user_id,
                 Item.num == item_id)
            ) .first()
    if not entry or entry.amount < amount:
        return False
    else:
        entry.amount = entry.amount - amount
    return True


def get_crystals(user_id, db: Session):
    entry = db\
        .query(EquipmentEntry)\
        .join(Item, EquipmentEntry.item)\
        .where(
             and_(
                 EquipmentEntry.owner_id == user_id,
                 Item.num == CRYSTAL)
            ) .first()
    if not entry:
        return 0
    return entry.amount


def get_item_entry(item_id, user_id, db: Session):
    return db\
        .query(EquipmentEntry)\
        .join(Item, EquipmentEntry.item)\
        .where(
             and_(
                 EquipmentEntry.owner_id == user_id,
                 Item.num == item_id)
            ) .first()
