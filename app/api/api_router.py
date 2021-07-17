from fastapi import APIRouter

from api.auth.auth_router import auth_router
from api.users.user_router import user_router

api_router = APIRouter()

api_router.include_router(user_router)
api_router.include_router(auth_router)
