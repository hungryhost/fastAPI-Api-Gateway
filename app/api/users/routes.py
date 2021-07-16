from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.auth.jwt_auth.dependencies import get_current_active_user
from app.api.schemas import User
from .response_models import Self
from app.database import get_db
from app.models.crud import get_user_by_id
from app.models.models import User as DbUser

router = APIRouter()


@router.get("/self/", response_model=Self)
def read_profile(
		user: User = Depends(get_current_active_user),
		db: Session = Depends(get_db), ) -> dict:
	db_user = get_user_by_id(db, user.id)
	return_dict = db_user.to_dict()
	if db_user.password is None:
		return_dict["has_password"] = False
	else:
		return_dict["has_password"] = True
	if db_user is None:
		raise HTTPException(status_code=404, detail="User not found")
	return return_dict
