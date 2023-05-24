from .manager import get_db
from ..routers.dto.user_schemas import AuthRequest
from .models import User


def create_user(user: AuthRequest):
    db = next(get_db())
    new_user = User(
            name=user.username,
            password=user.password
            )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
