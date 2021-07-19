from fastapi import APIRouter

from api.auth.jwt_auth.routes import router as jwt_router
from api.auth.oauth_google.routes import router as google_router

auth_router = APIRouter()

auth_router.include_router(jwt_router, tags=["jwt_auth"])
auth_router.include_router(google_router, tags=["google_auth"])
