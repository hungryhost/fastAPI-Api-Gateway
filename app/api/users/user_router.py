from fastapi import APIRouter

from users.routes import router

user_router = APIRouter()

user_router.include_router(router, tags=["users"])