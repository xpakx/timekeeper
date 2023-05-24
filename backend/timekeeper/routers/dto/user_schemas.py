from pydantic import BaseModel


class UserBase(BaseModel):
    username: str

    class Config:
        orm_mode = True


class AuthRequest(UserBase):
    password: str


class RegistrationRequest(AuthRequest):
    repeated_password: str


class AuthResponse(UserBase):
    token: str
