from typing import Union

from jose import jwt, JWTError
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from app.models.crud import get_user_by_email
from app.settings import settings
from app.schemas.auth_schemas import TokenModel
from app.schemas.core_schemas import User
from app.database import get_db
from sqlalchemy.orm import Session
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/internal/login/")


async def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db)) -> Union[HTTPException, User]:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.jwt_secret_key,
                             algorithms=[settings.jwt_algorithm])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenModel(email=email)

    except JWTError:
        raise credentials_exception
    user = get_user_by_email(db=db, email=token_data.email)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
        current_user: User = Depends(get_current_user)) -> Union[User, HTTPException]:
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


