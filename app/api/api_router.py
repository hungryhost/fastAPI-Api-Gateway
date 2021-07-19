from fastapi import APIRouter

from app.api.auth.auth_router import auth_router
from app.api.users.user_router import user_router

api_router = APIRouter()

api_router.include_router(user_router, prefix='/users')
api_router.include_router(auth_router, prefix='/auth')
