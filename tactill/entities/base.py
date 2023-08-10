from datetime import datetime
from typing import Annotated

import httpx
from pydantic import BaseModel, Field

TactillUUID = Annotated[str, Field(pattern=r"^[0-9A-Fa-f]{24}$")]


class BaseTactillModel(BaseModel):
    id: str = Field(alias="_id")
    version: int = Field(alias="__v")
    deprecated: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class ResponseValidation(BaseModel):
    source: str | None = None
    keys: list[str] | None = None


class TactillResponse(BaseModel):
    status_code: httpx.codes | None = Field(default=None, alias="statusCode")
    error: str | None = None
    message: str | None = None
    validation: ResponseValidation | None = None
