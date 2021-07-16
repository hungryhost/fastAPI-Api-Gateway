from datetime import datetime, timedelta
import string
import random
from typing import Optional

import jwt
from app.settings import settings


def generate_token(length: int = 24) -> str:
    return "".join(
        random.choice(string.ascii_uppercase + string.digits) for _ in range(length)
    )


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(seconds=settings.jwt_access_expiry)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
    return encoded_jwt


def create_refresh_token(data: dict):
    return create_access_token(data, expires_delta=timedelta(seconds=settings.jwt_refresh_expiry))

