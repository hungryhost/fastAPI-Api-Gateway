from pydantic import BaseModel, validator, EmailStr
from typing import Optional


class RegistrationModel(BaseModel):
    email: EmailStr
    password: str
    password_confirmation: str
    first_name: str
    last_name: str
    middle_name: Optional[str] = None

    @validator('password_confirmation')
    def passwords_match(cls, v, values, **kwargs):
        if 'password' in values and v != values['password']:
            raise ValueError('passwords do not match')
        return v

    @validator('password')
    def password_len(cls, v):
        assert len(v) >= 8, 'password must be at least 8 symbols'
        return v


class UserInfoResponseModel(BaseModel):
    id: Optional[int] = None
    email: EmailStr
    first_name: str
    last_name: str
    middle_name: Optional[str] = None
    picture: Optional[str] = None
    disabled: Optional[bool] = False
    google_auth: Optional[bool] = None
    hse_auth: Optional[bool] = None


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: Optional[str] = "bearer"


class RegistrationResponseModel(TokenModel):
    user_info: UserInfoResponseModel


class LoginModel(BaseModel):
    email: EmailStr
    password: str


class LoginResponseModel(TokenModel):
    user_info: UserInfoResponseModel


class TokenModel(BaseModel):
    email: Optional[EmailStr] = None

