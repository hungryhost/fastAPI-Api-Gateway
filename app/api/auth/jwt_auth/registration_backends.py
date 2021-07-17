from typing import Union

from sqlalchemy.orm import Session
from app.models.crud import get_user_by_email, create_user_jwt
from auth_schemas import RegistrationModel
from .password_authentication_backends import get_password_hash
from app.schemas.core_schemas import User as UserSchema


def create_user(db: Session, reg_info: RegistrationModel) -> Union[bool, UserSchema]:
	user = get_user_by_email(db, reg_info.email)
	if user:
		return False
	jwt_user = UserSchema(
		**reg_info.dict(exclude={'password', "password_confirmation"}),
		password=get_password_hash(reg_info.password))
	created_user = create_user_jwt(db=db, jwt_user=jwt_user)
	return UserSchema(**created_user.to_dict())
