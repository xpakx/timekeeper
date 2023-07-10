from .models import EquipmentEntry
from sqlalchemy.orm import Session


def create_entry(item_id, amount, user_id, db: Session):
    entry = EquipmentEntry(
            item_id=item_id,
            amount=amount,
            owner_id=user_id
            )
    db.add(entry)
    db.commit()
