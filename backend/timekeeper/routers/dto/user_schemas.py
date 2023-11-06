from pydantic import BaseModel, Field, validator


class UserBase(BaseModel):
    username: str = Field(min_length=4, max_lenth=20)

    class Config:
        orm_mode = True

    @validator('username')
    def validate_name_not_empty(cls, name: str):
        new_name = name.strip()
        if len(new_name) == 0:
            raise ValueError("Username cannot be empty")
        return new_name


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
