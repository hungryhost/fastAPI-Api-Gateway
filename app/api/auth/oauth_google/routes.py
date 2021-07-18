import json
import time
from typing import Union, Tuple

import httpx
import requests
from fastapi import APIRouter, Depends, status
from oauthlib.oauth2 import WebApplicationClient
from sqlalchemy.orm import Session
from starlette.requests import Request
from starlette.responses import JSONResponse
from app.schemas.oauth_schemas import LinkModel
from app.api.auth.jwt_auth.jwt_utils import create_jwt_pair
from app.database import get_db
from app.models.crud import get_user_by_email, create_user_google, update_user
from app.schemas.core_schemas import GoogleUser
from app.settings import settings
from app.schemas.auth_schemas import LoginResponseModel
from app.schemas.core_schemas import UserCoreSchema
from app.models.models import UserModel

LOGIN_URL = settings.google_login_url
REDIRECT_URL = f"{settings.app_url}/"
CONF_URL = settings.google_conf_url
oauth = WebApplicationClient(settings.google_client_id)
router = APIRouter()


def get_google_provider_cfg() -> dict:
	return requests.get(CONF_URL).json()


@router.get('/')
async def homepage(request: Request) -> dict:
	return {
		"error": "NO AUTH. PLEASE AUTHENTICATE YOURSELF",
		"code" : 401
	}


@router.get(
	path='/external/google/get-login-link/',
	response_model=LinkModel,
	status_code=status.HTTP_200_OK)
async def get_google_oauth_link() -> dict:
	google_provider_cfg: dict = get_google_provider_cfg()
	authorization_endpoint: str = google_provider_cfg["authorization_endpoint"]
	request_uri: str = oauth.prepare_request_uri(
		authorization_endpoint,
		redirect_uri=settings.app_url + settings.google_auth_path,
		scope=["openid", "email", "profile"],
	)
	return {"link": request_uri, "timestamp": str(time.time()), "status_code": 200}


@router.get('/external/google/', response_model=LoginResponseModel)
async def google_auth(
		request: Request,
		db: Session = Depends(get_db)) -> Union[JSONResponse, dict]:
	code: str = request.query_params.get("code")
	if code is None:
		return JSONResponse(content={
			'error': 'No code provided'
		},
			status_code=400
		)

	google_provider_cfg: dict = get_google_provider_cfg()
	token_endpoint: str = google_provider_cfg["token_endpoint"]
	request_url: str = str(request.url)
	request_base_url: str = str(request.base_url)

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
		userinfo_endpoint: str = google_provider_cfg["userinfo_endpoint"]
		uri, headers, body = oauth.add_token(userinfo_endpoint)
		userinfo_response = await client.post(uri, headers=headers, data=body)

	user: UserModel = get_user_by_email(db, userinfo_response.json()["email"])

	if user is None:
		if userinfo_response.json().get("email_verified"):
			# TODO: refactor the GoogleUser schema to pass all params from google response
			google_user: GoogleUser = GoogleUser(
				id=userinfo_response.json()["sub"],
				email=userinfo_response.json()["email"],
				first_name=userinfo_response.json()["given_name"],
				last_name=userinfo_response.json()["family_name"],
				picture=userinfo_response.json()["picture"]
			)
			user: UserModel = create_user_google(db, google_user)
		else:
			return JSONResponse(
				content={"User email not available or not verified by Google."},
				status_code=400)
	#if not user.picture:

	access_token, refresh_token = create_jwt_pair(
		data={"sub": user.email}
	)
	user_response: UserCoreSchema = UserCoreSchema(**user.to_dict())
	return {
		"access_token" : access_token,
		"refresh_token": refresh_token,
		"user_info"    : user_response.dict(exclude={'password'})
	}



