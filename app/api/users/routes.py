from fastapi import APIRouter, Depends, HTTPException
from oauthlib.oauth2 import WebApplicationClient
from sqlalchemy.orm import Session
from app.database import get_db
from app.settings import settings
from app.models.schemas import User
from app.api.auth.jwt_lib.dependencies import get_user_from_header
from app.models.models import User as DbUser
from app.models.crud import get_user_by_id

router = APIRouter()


@router.get("/me", response_model=User)
def read_profile(
		user: User = Depends(get_user_from_header),
		db: Session = Depends(get_db), ) -> DbUser:
	db_user = get_user_by_id(db, user.id)
	if db_user is None:
		raise HTTPException(status_code=404, detail="User not found")
	return db_user
