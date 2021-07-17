from typing import Union

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from app.api.auth.jwt_auth.jwt_utils import create_access_token, create_refresh_token
from app.database import get_db
from .password_authentication_backends import authenticate_user
from app.schemas.auth_schemas import RegistrationModel, LoginModel, RegistrationResponseModel, LoginResponseModel
from .registration_backends import create_user
router = APIRouter()


@router.post('/auth/internal/register/', response_model=RegistrationResponseModel)
async def register(
		registration_model: RegistrationModel,
		db: Session = Depends(get_db)) -> Union[HTTPException, dict]:
	user = create_user(db=db, reg_info=registration_model)
	if not user:
		raise HTTPException(
			status_code=status.HTTP_400_BAD_REQUEST,
			detail="User already exists.",
		)
	access_token = create_access_token(
		data={"sub": user.email}
	)
	refresh_token = create_refresh_token(
		data={"sub": user.email}
	)
	return {
		"access_token": access_token,
		"refresh_token": refresh_token,
		"user_info": user.dict(exclude={'password'})
	}


@router.post('/auth/internal/login/', response_model=LoginResponseModel)
async def login(
		login_model: LoginModel,
		db: Session = Depends(get_db)) -> Union[HTTPException, dict]:
	user = authenticate_user(db, login_model.email, login_model.password)
	if not user:
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="Incorrect username or password",
			headers={"WWW-Authenticate": "Bearer"},
		)
	access_token = create_access_token(
		data={"sub": user.email}
	)
	refresh_token = create_refresh_token(
		data={"sub": user.email}
	)
	return {
		"access_token": access_token,
		"refresh_token": refresh_token,
		"user_info": user.dict(exclude={'password'})
	}
