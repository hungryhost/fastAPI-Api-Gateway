from typing import Union
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from models.db_models import UserModel
from models.crud import get_user_by_email
from schemas.core_schemas import UserCoreSchema
import logging
import time

logging.basicConfig(level=logging.INFO)
name_logger = logging.getLogger(__name__)
name_logger.setLevel(logging.INFO)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> CryptContext:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> CryptContext:
    return pwd_context.hash(password)


def authenticate_user(db: Session, email: str, password: str) -> Union[bool, UserCoreSchema]:
    start = time.time()
    user: UserModel = get_user_by_email(db, email)
    end = time.time()
    name_logger.warning("got user in {}".format(end - start))
    if not user:
        return False
    start = time.time()
    if not verify_password(plain_password=password, hashed_password=user.password):
        return False
    end = time.time()
    name_logger.warning("verified pass in {}".format(end - start))
    return UserCoreSchema(**user.to_dict())
