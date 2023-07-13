from .models import EquipmentEntry
from sqlalchemy.orm import Session
from sqlalchemy import and_


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
