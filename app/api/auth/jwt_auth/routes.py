from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from app.api.auth.jwt_auth.jwt_utils import create_access_token
from app.database import get_db
from .password_authentication_backends import authenticate_user
from .schemas import RegistrationModel, LoginModel

router = APIRouter()


@router.post('/auth/internal/register/')
async def register(registration_model: RegistrationModel):
	return registration_model


@router.post('/auth/internal/login/')
async def login(login_model: LoginModel, db: Session = Depends(get_db)):
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
	return {"access_token": access_token, "token_type": "bearer"}
