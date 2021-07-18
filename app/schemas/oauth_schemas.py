from pydantic import BaseModel
from typing import Generic, TypeVar, Optional, List
from pydantic.generics import GenericModel


class BaseResponseClass(BaseModel):
	status_code: int
	timestamp: str


class LinkModel(BaseResponseClass):
	link: str

