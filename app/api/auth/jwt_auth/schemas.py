from pydantic import BaseModel
from typing import Optional


class RegistrationModel(BaseModel):
    email: str
    password: str
    password_confirmation: str
    first_name: str
    last_name: str
    middle_name: Optional[str] = None


class LoginModel(BaseModel):
    email: str
    password: str


class TokenModel(BaseModel):
    email: Optional[str] = None

