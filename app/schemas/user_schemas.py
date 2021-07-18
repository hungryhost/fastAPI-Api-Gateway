from typing import Optional

from pydantic import BaseModel, EmailStr, validator


class Self(BaseModel):
    id: int
    email: EmailStr
    first_name: str
    last_name: str
    middle_name: Optional[str] = None
    picture: Optional[str] = None
    disabled: bool
    has_password: bool
    hse_auth: bool
    google_auth: bool

    class Config:
        orm_mode = True


class UserUpdateSchemaRequest(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    middle_name: Optional[str]
    picture: Optional[str] = None


class UserUpdateSchema(UserUpdateSchemaRequest):
    id: int
    hse_auth: bool
    google_auth: bool


class UserSetPasswordRequestSchema(BaseModel):
    password: str
    password_confirmation: str

    @validator('password_confirmation')
    def passwords_match(cls, v, values, **kwargs):
        if 'password' in values and v != values['password']:
            raise ValueError('passwords do not match')
        return v

    @validator('password')
    def password_len(cls, v):
        assert len(v) >= 8, 'password must be at least 8 symbols'
        return v


class UserSetPasswordSchema(BaseModel):
    id: int
    password: str
