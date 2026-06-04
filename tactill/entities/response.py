import httpx
from pydantic import BaseModel, Field


class TactillResponse(BaseModel):
    status_code: httpx.codes = Field(alias="statusCode")
    error: str
    message: str
