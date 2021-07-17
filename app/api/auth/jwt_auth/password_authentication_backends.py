from typing import Union

from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.models.crud import get_user_by_email
from app.schemas.core_schemas import User as UserSchema
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> CryptContext:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> CryptContext:
    return pwd_context.hash(password)


def authenticate_user(db: Session, email: str, password: str) -> Union[bool, UserSchema]:
    user = get_user_by_email(db, email)
    if not user:
        return False
    if not verify_password(plain_password=password, hashed_password=user.password):
        return False
    return UserSchema(**user.to_dict())
