from typing import List, Optional, Union

from sqlalchemy.orm import Session


from .models import UserModel
from app.schemas.core_schemas import GoogleUser
from app.schemas.core_schemas import User as JwtUser
from app.schemas.user_schemas import UserUpdateSchema, UserSetPasswordSchema


def get_user_by_id(db: Session, user_id: int) -> Optional[UserModel]:
    return db.query(UserModel).filter_by(id=user_id).first()


def get_user_by_email(db: Session, email: str) -> Optional[UserModel]:
    return db.query(UserModel).filter_by(email=email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[UserModel]:
    return db.query(UserModel).offset(skip).limit(limit).all()




def create_user_google(db: Session, google_user: GoogleUser) -> UserModel:
    user = UserModel(
        email=google_user.email,
        first_name=google_user.first_name,
        last_name=google_user.last_name,
        google_auth=True,
        hse_auth=False,
        picture=google_user.picture,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def create_user_jwt(db: Session, jwt_user: JwtUser) -> UserModel:
    user = UserModel(
        email=jwt_user.email,
        first_name=jwt_user.first_name,
        password=jwt_user.password,
        last_name=jwt_user.last_name,
        middle_name=jwt_user.middle_name,
        google_auth=False,
        hse_auth=False,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    return user
