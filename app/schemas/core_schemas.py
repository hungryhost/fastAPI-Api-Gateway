from pydantic import BaseModel, EmailStr
from typing import Optional


class Url(BaseModel):
    url: str


class AuthorizationResponse(BaseModel):
    state: str
    code: str


class GoogleUser(BaseModel):
    id: int
    email: EmailStr
    first_name: str
    last_name: str
    picture: str


class UserInfoSchema(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    middle_name: Optional[str] = None
    picture: Optional[str] = None
    disabled: Optional[bool] = False
    google_auth: Optional[bool] = False
    hse_auth: Optional[bool] = False


class UserCoreSchema(UserInfoSchema):
    id: int


class User(UserInfoSchema):
    password: str

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str
    user: User
