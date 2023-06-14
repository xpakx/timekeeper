from ..routers.dto import user_schemas
from ..db import user_repo
from jose import jwt, JWTError
from datetime import datetime, timedelta
from typing import Optional
from ..security.jwt import SECRET
from sqlalchemy.orm import Session
from fastapi import status, HTTPException


def login(
        request: user_schemas.AuthRequest,
        db: Session) -> user_schemas.AuthResponse:
    user = user_repo.check_user(request, db)
    if user:
        token = create_token({"sub": user.username, "id": user.id})
        refresh_token = create_refresh_token({"id": user.id})
        response = user_schemas.AuthResponse(
                username=request.username,
                token=token,
                refresh_token=refresh_token)
        return response
    else:
        raise no_user_exception()


def register(
        request: user_schemas.RegistrationRequest,
        db: Session) -> Optional[user_schemas.AuthResponse]:
    if request.password != request.repeated_password:
        raise wrong_repeated_password_exception()
    user = user_repo.create_user(request, db)
    if user:
        token = create_token({"sub": user.username, "id": user.id})
        refresh_token = create_refresh_token({"id": user.id})
        response = user_schemas.AuthResponse(
                username=request.username,
                token=token,
                refresh_token=refresh_token)
        return response
    return None


def refresh(request, db: Session) -> Optional[user_schemas.AuthResponse]:
    try:
        claims = jwt.decode(request.refresh_token, SECRET, algorithms=["HS256"])
        user = user_repo.get_user_by_id(int(claims.get('id')), db)
        if user:
            token = create_token({"sub": user.username, "id": user.id})
            refresh_token = create_refresh_token({"id": user.id})
            response = user_schemas.AuthResponse(
                    username=user.username,
                    token=token,
                    refresh_token=refresh_token)
            return response
        raise not_refreshed()
    except JWTError:
        raise not_refreshed()


def create_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET, algorithm="HS256")
    return encoded_jwt


def create_refresh_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=7)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET, algorithm="HS256")
    return encoded_jwt


def no_user_exception():
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User not found",
    )


def wrong_repeated_password_exception():
    return HTTPException(
        status_code=400,
        detail="Passwords should be the same",
    )


def not_refreshed():
    return HTTPException(
        status_code=401,
        detail="Could not refresh token",
    )
