from ..routers.dto.user_schemas import AuthRequest, RegistrationRequest
from .models import User
from bcrypt import hashpw, checkpw, gensalt
from typing import Optional
from sqlalchemy.orm import Session


def create_user(user: RegistrationRequest, db: Session) -> User:
    hashed_password = hashpw(user.password.encode('utf-8'), gensalt())
    new_user = User(
            username=user.username,
            password=hashed_password
            )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def check_user(user: AuthRequest, db: Session) -> Optional[User]:
    db_user = db.query(User).where(User.username == user.username).first()
    if checkpw(user.password.encode('utf-8'), db_user.password.encode('utf-8')):
        return db_user
    return None
