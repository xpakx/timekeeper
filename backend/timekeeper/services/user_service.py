from ..routers.dto import user_schemas
from ..db import user_repo
from jose import jwt
from datetime import datetime, timedelta
from typing import Optional
from ..security.jwt import SECRET
from sqlalchemy.orm import Session


def login(request: user_schemas.AuthRequest, db: Session) -> Optional[user_schemas.AuthResponse]:
    user = user_repo.check_user(request)
    if user:
        token = create_token({"sub": user.username, "id": user.id})
        response = user_schemas.AuthResponse()
        response.username = request.username
        response.token = token
        return response
    return None


def register(request: user_schemas.RegistrationRequest, db: Session):
    return user_repo.create_user(request)


def create_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET, algorithm="HS256")
    return encoded_jwt
