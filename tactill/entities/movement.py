import datetime
from enum import StrEnum

from pydantic import BaseModel

from tactill.entities.base import BaseTactillModel, TactillName, TactillUUID


class MovementType(StrEnum):
    IN = "in"
    OUT = "out"


class MovementState(StrEnum):
    PLANNED = "planned"
    PARTIAL = "partial"
    DONE = "done"


class MovementMotive(StrEnum):
    TRANSFER = "transfer"
    UNSALEABLE = "unsaleable"
    FAULTY = "faulty"
    UNSET = "unset"
    UNDEFINED = ""


class ArticleMovement(BaseModel):
    article_id: TactillUUID
    article_name: TactillName
    category_name: TactillName
    state: MovementState
    units: int
    done_on: datetime.datetime | None = None


class MovementCreation(BaseModel):
    type: MovementType
    state: MovementState
    motive: MovementMotive
    movements: list[ArticleMovement]


class Movement(BaseTactillModel):
    number: int
    type: MovementType
    state: MovementState
    motive: MovementMotive = MovementMotive.UNSET
    movements: list[ArticleMovement]
