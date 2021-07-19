from typing import Union

from sqlalchemy.orm import Session
from models.crud import get_user_by_email, create_user_jwt
from models.db_models import UserModel
from schemas.auth_schemas import RegistrationModel
from .password_authentication_backends import get_password_hash
from schemas.core_schemas import User as UserSchema
from schemas.core_schemas import UserCoreSchema


def create_user(db: Session, reg_info: RegistrationModel) -> Union[bool, UserCoreSchema]:
	user: UserModel = get_user_by_email(db, reg_info.email)
	if user:
		return False

	jwt_user: UserSchema = UserSchema(
		**reg_info.dict(exclude={'password', "password_confirmation"}),
		password=get_password_hash(reg_info.password))
	created_user: UserModel = create_user_jwt(db=db, jwt_user=jwt_user)
	return UserCoreSchema(**created_user.to_dict())
