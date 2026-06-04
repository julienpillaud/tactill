import datetime
from enum import StrEnum
from typing import Annotated

from pydantic import BaseModel, Field

TactillUUID = Annotated[str, Field(pattern=r"^[0-9A-Fa-f]{24}$")]
TactillName = Annotated[str, Field(min_length=1)]
IconText = Annotated[str, Field(min_length=1, max_length=4)]


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


class BaseEntity(BaseModel):
    id: TactillUUID = Field(alias="_id")
    deprecated: bool = False
    created_at: datetime.datetime
    updated_at: datetime.datetime
