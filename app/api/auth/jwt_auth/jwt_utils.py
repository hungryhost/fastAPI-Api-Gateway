from datetime import datetime, timedelta
import string
import random
from typing import Optional, Tuple
from fastapi import HTTPException, status
from jose import jwt, JWTError


from app.settings import settings


def generate_token(length: int = 24) -> str:
    return "".join(
        random.choice(string.ascii_uppercase + string.digits) for _ in range(length)
    )


def create_access_token(data: dict, expires_delta: Optional[int] = None) -> str:
    to_encode: dict = data.copy()
    if expires_delta:
        expire: datetime = datetime.utcnow() + timedelta(seconds=expires_delta)
    else:
        expire: datetime = datetime.utcnow() + timedelta(seconds=settings.jwt_access_expiry)
    to_encode.update({"exp": expire})
    encoded_jwt: str = jwt.encode(to_encode, settings.jwt_secret_key,
                             algorithm=settings.jwt_algorithm)
    return encoded_jwt


def create_refresh_token(data: dict) -> str:
    return create_access_token(data, expires_delta=settings.jwt_refresh_expiry)


def create_jwt_pair(data: dict) -> Tuple[str, str]:
    """
    Parameters
    ----------
    :param data: dict
        data to encode in jwt. Must contain "sub" key with user's email.
    :return: Tuple[bytes, bytes]
        a tuple of tokens as bytes objects
    """
    if 'sub' not in data.keys():
        raise Exception("sub not in jwt data keys")
    return (create_access_token(data=data),
            create_refresh_token(data=data))


def issue_new_token(refresh_token: str):
    credentials_exception: HTTPException = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload: dict = jwt.decode(refresh_token, settings.jwt_secret_key,
                                   algorithms=[settings.jwt_algorithm])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return create_access_token(data=payload)
