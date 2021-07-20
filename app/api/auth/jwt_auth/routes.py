from typing import Union

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from api.auth.jwt_auth.jwt_utils import create_jwt_pair, issue_new_token
from database import get_db
from .password_authentication_backends import authenticate_user
from schemas.core_schemas import UserCoreSchema
from schemas.auth_schemas import RegistrationModel, LoginModel, RegistrationResponseModel, LoginResponseModel, \
	TokenRefreshRequestModel, TokenRefreshResponseModel
from .registration_backends import create_user

router = APIRouter()


@router.post('/internal/register/', response_model=RegistrationResponseModel)
def register(
		registration_model: RegistrationModel,
		db: Session = Depends(get_db)) -> Union[HTTPException, dict]:
	user: Union[bool, UserCoreSchema] = create_user(db=db, reg_info=registration_model)
	if not user:
		raise HTTPException(
			status_code=status.HTTP_400_BAD_REQUEST,
			detail="User already exists.",
		)
	access_token, refresh_token = create_jwt_pair(
		data={"sub": user.email}
	)

	return {
		"access_token": access_token,
		"refresh_token": refresh_token,
		"user_info": user.dict()
	}


@router.post('/internal/login/', response_model=LoginResponseModel)
def login(
		login_model: LoginModel,
		db: Session = Depends(get_db)) -> Union[HTTPException, dict]:
	user: UserCoreSchema = authenticate_user(db, login_model.email, login_model.password)
	if not user:
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="Incorrect username or password",
			headers={"WWW-Authenticate": "Bearer"},
		)
	access_token, refresh_token = create_jwt_pair(
		data={"sub": user.email}
	)
	return {
		"access_token": access_token,
		"refresh_token": refresh_token,
		"user_info": user.dict()
	}


@router.post('/internal/refresh/', response_model=TokenRefreshResponseModel)
def refresh_token(
		refresh_token_data: TokenRefreshRequestModel) -> Union[HTTPException, dict]:
	return {"access_token": issue_new_token(refresh_token=refresh_token_data.refresh_token)}
