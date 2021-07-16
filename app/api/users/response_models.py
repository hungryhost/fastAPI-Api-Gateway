from pydantic import BaseModel
from typing import Generic, TypeVar, Optional, List
from pydantic.generics import GenericModel


class Self(BaseModel):
    id: int
    email: str
    first_name: str
    last_name: Optional[str] = None
    middle_name: Optional[str] = None
    picture: str
    disabled: bool
    has_password: bool

    class Config:
        orm_mode = True
