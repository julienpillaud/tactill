from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, Field

TactillUUID = Annotated[str, Field(pattern=r"^[0-9A-Fa-f]{24}$")]


class BaseTactillModel(BaseModel):
    id: str = Field(alias="_id")
    version: int = Field(alias="__v")
    deprecated: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
