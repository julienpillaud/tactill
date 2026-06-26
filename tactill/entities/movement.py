import datetime
from enum import StrEnum

from pydantic import BaseModel

from tactill.entities.base import BaseEntity, TactillName, TactillUUID


class MovementType(StrEnum):
    IN = "in"
    OUT = "out"


class MovementState(StrEnum):
    PLANNED = "planned"
    PARTIAL = "partial"
    DONE = "done"


class MovementMotive(StrEnum):
    TRANSFER = "transfer"
    UNDEFINED = ""


class ArticleMovement(BaseModel):
    article_id: TactillUUID
    article_name: TactillName
    category_name: TactillName
    state: MovementState
    units: int
    done_on: datetime.datetime


class MovementCreate(BaseModel):
    type: MovementType
    state: MovementState
    motive: MovementMotive
    movements: list[ArticleMovement]


class Movement(BaseEntity):
    number: int
    type: MovementType
    state: MovementState
    motive: MovementMotive | None = None
    movements: list[ArticleMovement]
