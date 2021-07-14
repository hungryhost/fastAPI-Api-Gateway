from pydantic import BaseModel


class Url(BaseModel):
    url: str


class AuthorizationResponse(BaseModel):
    state: str
    code: str


class GoogleUser(BaseModel):
    id: int
    email: str
    first_name: str
    picture: str


class User(BaseModel):
    id: int
    email: str
    first_name: str
    picture: str

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str
    user: User