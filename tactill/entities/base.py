import datetime
from enum import StrEnum
from typing import Annotated

import httpx
from pydantic import BaseModel, Field

TactillUUID = Annotated[str, Field(pattern=r"^[0-9A-Fa-f]{24}$")]
IconText = Annotated[str, Field(min_length=1)]
TactillName = Annotated[str, Field(min_length=1)]


class TactillColor(StrEnum):
    GREEN = "#57DB47"
    PURPLE = "#6868DC"
    TEAL = "#30BEA5"
    PINK = "#F44F60"
    BLUE = "#1E8CFF"
    YELLOW = "#F2BA43"
    MAGENTA = "#B455C8"
    ORANGE = "#FF6347"
    BROWN = "#A06E58"
    GRAY = "#9EA09E"


class BaseTactillModel(BaseModel):
    id: TactillUUID = Field(alias="_id")
    deprecated: bool = False
    created_at: datetime.datetime
    updated_at: datetime.datetime


class ResponseValidation(BaseModel):
    source: str | None = None
    keys: list[str] | None = None


class TactillResponse(BaseModel):
    status_code: httpx.codes | None = Field(default=None, alias="statusCode")
    error: str | None = None
    message: str | None = None
    validation: ResponseValidation | None = None
