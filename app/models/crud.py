from typing import List, Optional

from sqlalchemy.orm import Session


from .models import User
from .schemas import GoogleUser


def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    return db.query(User).filter_by(id=user_id).first()


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter_by(email=email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
    return db.query(User).offset(skip).limit(limit).all()


def create_user_google(db: Session, google_user: GoogleUser) -> User:
    user = User(
        email=google_user.email,
        first_name=google_user.first_name,
        google_auth=True,
        hse_auth=False,
        picture=google_user.picture,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    return user
