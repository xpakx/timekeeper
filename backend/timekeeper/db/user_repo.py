from .manager import get_db
from ..routers.dto.user_schemas import AuthRequest, RegistrationRequest
from .models import User
from bcrypt import hashpw, checkpw, gensalt
from typing import Optional


def create_user(user: RegistrationRequest) -> User:
    db = next(get_db())
    hashed_password = hashpw(user.password.encode('utf-8'), gensalt())
    new_user = User(
            name=user.username,
            password=hashed_password
            )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def check_user(user: AuthRequest) -> Optional[User]:
    db = next(get_db())
    db_user = db.query(User).where(User.username == user.username).first()
    if checkpw(user.password.encode('utf-8'), db_user.password.encode('utf-8')):
        return db_user
    return None
