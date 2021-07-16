from passlib.context import CryptContext
from app.models.crud import get_user_by_email

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> CryptContext:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> CryptContext:
    return pwd_context.hash(password)


def authenticate_user(fake_db, email: str, password: str):
    user = get_user_by_email(fake_db, email)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user