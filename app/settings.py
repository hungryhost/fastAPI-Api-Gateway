from authlib.integrations.starlette_client import OAuth
from pydantic import BaseSettings, Field
from starlette.config import Config


class Settings(BaseSettings):
    env: str = Field("prod", env="ENV")
    app_url: str = Field("http://127.0.0.1:8000/", env="APP_URL")
    db_uri: str = Field(
        "postgresql://admin:admin@localhost:5432/fastapi", env="DB_URI"
    )
    google_client_id: str = Field("", env="GOOGLE_CLIENT_ID")
    google_client_secret: str = Field("", env="GOOGLE_CLIENT_SECRET")
    jwt_secret_key: str = Field("example_key_super_secret", env="SECRET_KEY")
    jwt_algorithm: str = Field("HS256", env="ALGORITHM")
    google_auth_path: str = Field("auth/google", env="GOOGLE_AUTH_CALLBACK_PATH")
    google_conf_url: str = Field("https://accounts.google.com/.well-known/openid-configuration",
                                 env="GOOGLE_CONF_URL")
    google_login_url: str = Field("https://accounts.google.com/o/oauth2/v2/auth",
                                  env="GOOGLE_LOGIN_URL")

    class Config:
        env_file = '.env'


settings = Settings()

