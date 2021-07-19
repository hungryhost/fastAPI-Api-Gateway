from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.auth.jwt_auth.dependencies import get_current_active_user
from api.auth.jwt_auth.password_authentication_backends import get_password_hash
from models.db_models import UserModel
from schemas.user_schemas import Self, UserUpdateSchema, UserUpdateSchemaRequest, UserSetPasswordSchema, \
	UserSetPasswordRequestSchema
from database import get_db
from models.crud import get_user_by_id, update_user

router = APIRouter()


@router.get("/self/", response_model=Self)
def read_profile(
		user: UserModel = Depends(get_current_active_user),
		db: Session = Depends(get_db), ) -> dict:
	db_user: UserModel = get_user_by_id(db, user.id)
	return_dict: dict = db_user.to_dict()
	if db_user.password is None:
		return_dict["has_password"] = False
	else:
		return_dict["has_password"] = True
	if db_user is None:
		raise HTTPException(status_code=404, detail="User not found")
	return return_dict


@router.put("/self/", response_model=Self)
def update_profile(
		update_info: UserUpdateSchemaRequest,
		user: UserModel = Depends(get_current_active_user),
		db: Session = Depends(get_db), ) -> dict:
	db_user: UserModel = get_user_by_id(db, user.id)

	db_user_model: UserUpdateSchema = UserUpdateSchema(**db_user.to_dict())
	update_data: dict = update_info.dict(exclude_unset=True)
	updated_info: UserUpdateSchema = db_user_model.copy(update=update_data)
	if user.email != updated_info.email:
		raise HTTPException(
			status_code=400,
			detail="Cannot change email with external auth.")
	user: UserModel = update_user(db, updated_user=updated_info)
	return_dict: dict = user.to_dict()

	if user.password is None:
		return_dict["has_password"] = False
	else:
		return_dict["has_password"] = True
	return return_dict


@router.post("/self/set-password/")
def set_password(
		update_info: UserSetPasswordRequestSchema,
		user: UserModel = Depends(get_current_active_user),
		db: Session = Depends(get_db), ) -> dict:
	db_user: UserModel = get_user_by_id(db, user.id)
	if db_user.password:
		raise HTTPException(
			status_code=400,
			detail="User already has password.")
	password_data = UserSetPasswordSchema(
		id=user.id,
		password=get_password_hash(update_info.password)
	)
	user: UserModel = update_user(db, updated_user=password_data)

	return {"result": "OK"}
