from pydantic import BaseModel, Field


class UserBase(BaseModel):
    username: str = Field(min_length=4, max_lenth=20)

    class Config:
        orm_mode = True


class AuthRequest(UserBase):
    password: str = Field(min_length=1)


class RegistrationRequest(AuthRequest):
    repeated_password: str


class AuthResponse(UserBase):
    token: str
    refresh_token: str


class RefreshRequest(BaseModel):
    refresh_token: str

    class Config:
        orm_mode = True
