import httpx2
from pydantic import BaseModel, Field


class TactillResponse(BaseModel):
    status_code: httpx2.codes = Field(alias="statusCode")
    error: str
    message: str
