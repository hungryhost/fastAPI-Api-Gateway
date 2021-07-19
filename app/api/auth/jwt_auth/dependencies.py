from typing import Union

from jose import jwt, JWTError
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from models.crud import get_user_by_email
from settings import settings
from schemas.auth_schemas import TokenDataModel
from models.db_models import UserModel
from database import get_db
from sqlalchemy.orm import Session
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/internal/register/")


async def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db)) -> Union[HTTPException, UserModel]:
    credentials_exception: HTTPException = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload: dict = jwt.decode(token, settings.jwt_secret_key,
                             algorithms=[settings.jwt_algorithm])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenDataModel(email=email)

    except JWTError:
        raise credentials_exception
    user: UserModel = get_user_by_email(db=db, email=token_data.email)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
        current_user: UserModel = Depends(get_current_user)) -> Union[UserModel, HTTPException]:
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


