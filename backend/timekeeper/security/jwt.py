from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from typing import Annotated

SECRET = "F8eTVCgV2ifLas"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class CurrentUser():
    username: str
    id: int


async def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)]) -> CurrentUser:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET, algorithms=["HS256"])
        user = CurrentUser()
        user.username = payload.get("sub")
        if user.username is None:
            raise credentials_exception
        user.id = int(payload.get("id"))
        return user
    except JWTError:
        raise credentials_exception
