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

from app.database import get_db
from app.settings import settings

oauth = WebApplicationClient(settings.google_client_id)

from app.models.schemas import User
from app.models.crud import get_user_by_id
from app.auth.jwt.dependencies import get_user_from_header
from app.models.models import User as DbUser

LOGIN_URL = settings.google_login_url
REDIRECT_URL = f"{settings.app_url}/"
CONF_URL = settings.google_conf_url

router = APIRouter()


def get_google_provider_cfg():
    return requests.get(CONF_URL).json()


"""
@router.get("/login")
def get_login_url() -> Url:
    params = {
        "client_id": settings.google_client_id,
        "redirect_uri": REDIRECT_URL,
        "state": generate_token(),
    }
    return Url(url=f"{LOGIN_URL}?{urlencode(params)}")
"""


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
async def auth(request: Request):

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
        userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
        uri, headers, body = oauth.add_token(userinfo_endpoint)
        userinfo_response = await client.post(uri, headers=headers, data=body)

    user_dict = {}
    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        picture = userinfo_response.json()["picture"]
        users_name = userinfo_response.json()["given_name"]
        user_dict = {
            'g_id'   : unique_id,
            'g_email': users_email,
            'g_pic'  : picture,
            'g_name' : users_name
        }
        response_dict = {
            "user"                 : user_dict,
            "timestamp"            : datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f%z'),
            "unix_timestamp"       : time.time(),
            "access_token"         : "NOT GENERATED",
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


"""
@router.post("/authorize")
async def verify_authorization(
    body: AuthorizationResponse, db: Session = Depends(get_db)
) -> Token:
    params = {
        "client_id": settings.google_client_id,
        "client_secret": settings.google_client_secret,
        "code": body.code,
        "state": body.state,
    }

    async with httpx.AsyncClient() as client:
        token_request = await client.post(TOKEN_URL, params=params)
        response: Dict[bytes, bytes] = dict(parse_qsl(token_request.content))
        github_token = response[b"access_token"].decode("utf-8")
        github_header = {"Authorization": f"token {github_token}"}
        user_request = await client.get(USER_URL, headers=github_header)
        github_user = GithubUser(**user_request.json())

    db_user = get_user_by_login(db, github_user.login)
    if db_user is None:
        db_user = create_user(db, github_user)

    verified_user = User.from_orm(db_user)
    access_token = create_access_token(data=verified_user)

    return Token(access_token=access_token, token_type="bearer", user=db_user)

"""


@router.get("/me", response_model=User)
def read_profile(
        user: User = Depends(get_user_from_header),
        db: Session = Depends(get_db),) -> DbUser:
    db_user = get_user(db, user.id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
