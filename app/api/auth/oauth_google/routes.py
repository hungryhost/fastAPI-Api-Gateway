import datetime
import json
import time

import httpx
import requests
from fastapi import APIRouter, Depends
from oauthlib.oauth2 import WebApplicationClient
from sqlalchemy.orm import Session
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.api.auth.jwt_lib.helpers import create_access_token
from app.database import get_db
from app.models.crud import get_user_by_email, create_user_google
from app.models.schemas import User, GoogleUser
from app.settings import settings

LOGIN_URL = settings.google_login_url
REDIRECT_URL = f"{settings.app_url}/"
CONF_URL = settings.google_conf_url
oauth = WebApplicationClient(settings.google_client_id)
router = APIRouter()


def get_google_provider_cfg():
    return requests.get(CONF_URL).json()


@router.get('/')
async def homepage(request: Request):
    return {
        "error": "NO AUTH. PLEASE AUTHENTICATE YOURSELF",
        "code" : 401
    }


@router.get('/auth/google/login')
async def login():
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]
    request_uri = oauth.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=settings.app_url + settings.google_auth_path,
        scope=["openid", "email", "profile"],
    )
    return request_uri


@router.get('/auth/google')
async def auth(request: Request, db: Session = Depends(get_db)):

    code = request.query_params.get("code")
    if code is None:
        return JSONResponse(content={
            'error': 'No code provided'
        },
            status_code=400
        )

    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]
    request_url = str(request.url)
    request_base_url = str(request.base_url)

    async with httpx.AsyncClient() as client:

        token_url, headers, body = oauth.prepare_token_request(
            token_endpoint,
            authorization_response=request_url,
            redirect_url=request_base_url + settings.google_auth_path,
            code=code
        )
        token_response = await client.post(
            token_url,
            headers=headers,
            data=body,
            auth=(settings.google_client_id, settings.google_client_secret),
        )
        # Parse the tokens!
        oauth.parse_request_body_response(json.dumps(token_response.json()))
        # print(json.dumps(token_response.json()))
        userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
        uri, headers, body = oauth.add_token(userinfo_endpoint)
        userinfo_response = await client.post(uri, headers=headers, data=body)
    user = get_user_by_email(db, userinfo_response.json()["email"])
    google_user = GoogleUser(
        id=userinfo_response.json()["sub"],
        email=userinfo_response.json()["email"],
        first_name=userinfo_response.json()["given_name"],
        picture=userinfo_response.json()["picture"]
    )
    if user is None:
        user = create_user_google(db, google_user)

    if userinfo_response.json().get("email_verified"):
        verified_user = User.from_orm(user)
        access_token = create_access_token(data=verified_user)
        response_dict = {
            "user"                 : google_user.to_dict(),
            "timestamp"            : datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f%z'),
            "unix_timestamp"       : time.time(),
            "access_token"         : access_token.decode('utf-8'),
            "token_type"           : "bearer",
            "refresh_token"        : "NOT GENERATED",
            "access_token_expires" : (datetime.datetime.now() + datetime.timedelta(minutes=30)).strftime(
                '%Y-%m-%dT%H:%M:%S.%f%z'),
            "refresh_token_expires": (datetime.datetime.now() + datetime.timedelta(hours=24)).strftime(
                '%Y-%m-%dT%H:%M:%S.%f%z')
        }
        return JSONResponse(content=response_dict, status_code=200)
    else:
        return JSONResponse(content={"User email not available or not verified by Google."},
                            status_code=400)