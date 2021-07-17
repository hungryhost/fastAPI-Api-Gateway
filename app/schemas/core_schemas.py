from pydantic import BaseModel
from typing import Optional


class Url(BaseModel):
    url: str


class AuthorizationResponse(BaseModel):
    state: str
    code: str


class GoogleUser(BaseModel):
    id: int
    email: str
    first_name: str
    last_name: str
    picture: str


class User(BaseModel):
    id: int
    email: str
    first_name: str
    last_name: str
    middle_name: Optional[str] = None
    picture: Optional[str] = None
    disabled: Optional[bool] = False
    password: Optional[str] = None
    google_auth: Optional[bool] = False
    hse_auth: Optional[bool] = False

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str
    user: User
