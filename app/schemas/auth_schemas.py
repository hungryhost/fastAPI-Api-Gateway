from pydantic import BaseModel, validator, EmailStr
from typing import Optional
from app.schemas.core_schemas import UserCoreSchema
from app.settings import settings


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


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: Optional[str] = "bearer"
    access_token_expiry: Optional[int] = settings.jwt_access_expiry
    refresh_token_expiry: Optional[int] = settings.jwt_refresh_expiry


class RegistrationResponseModel(TokenModel):
    user_info: UserCoreSchema


class LoginModel(BaseModel):
    email: EmailStr
    password: str


class LoginResponseModel(TokenModel):
    user_info: UserCoreSchema


class TokenDataModel(BaseModel):
    email: Optional[EmailStr] = None


class TokenRefreshRequestModel(BaseModel):
    refresh_token: str
    grant_type: str


class TokenRefreshResponseModel(BaseModel):
    access_token: str
    access_token_expiry: Optional[int] = settings.jwt_access_expiry
