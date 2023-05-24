from .manager import get_db
from ..routers.dto.user_schemas import AuthRequest, RegistrationRequest
from .models import User


def create_user(user: RegistrationRequest) -> User:
    db = next(get_db())
    new_user = User(
            name=user.username,
            password=user.password
            )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def check_user(user: AuthRequest) -> bool:
    db = next(get_db())
    db_user = db.query(User).where(User.username == user.username).first()
    if db_user.password == user.password:
        return True
    return False
