import datetime
from typing import Annotated, Literal

import httpx
from pydantic import BaseModel, Field

TactillUUID = Annotated[str, Field(pattern=r"^[0-9A-Fa-f]{24}$")]
TactillColor = Literal[
    "#57DB47",
    "#6868DC",
    "#30BEA5",
    "#F44F60",
    "#1E8CFF",
    "#F2BA43",
    "#B455C8",
    "#FF6347",
    "#A06E58",
    "#9EA09E",
]


def datetime_utcnow():
    return datetime.datetime.now(tz=datetime.UTC)


class BaseTactillModel(BaseModel):
    id: str = Field(alias="_id")
    version: int = Field(alias="__v")
    deprecated: bool = False
    created_at: datetime.datetime = Field(default_factory=datetime_utcnow)
    updated_at: datetime.datetime = Field(default_factory=datetime_utcnow)
    original_id: str | None = None


class ResponseValidation(BaseModel):
    source: str | None = None
    keys: list[str] | None = None


class TactillResponse(BaseModel):
    status_code: httpx.codes | None = Field(default=None, alias="statusCode")
    error: str | None = None
    message: str | None = None
    validation: ResponseValidation | None = None
