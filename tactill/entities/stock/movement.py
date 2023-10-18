from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field

from tactill.entities.base import BaseTactillModel, TactillUUID

MovementType = Literal["", "in", "out"]
MovementState = Literal["planned", "partial", "done"]
MovementMotive = Literal["transfer", "unsaleable", "faulty"]
MovementDeviceType = Literal["iphone", "ipad", "backoffice"]


def datetime_to_string() -> str:
    return datetime.utcnow().isoformat()


class ArticleMovement(BaseModel):
    article_id: TactillUUID
    declination_id: str | None = None
    article_name: str
    declination_name: str | None = None
    category_name: str
    reference: str | None = None
    barcode: str | None = None
    state: MovementState
    units: float
    planned_on: str | None = None
    done_on: str = Field(default_factory=datetime_to_string)  # error on documentation
    device_type: MovementDeviceType | None = None
    device_name: str | None = None
    account_name: str | None = None
    buy_price: float | None = None
    out_price: float | None = None


class BaseMovement(BaseModel):
    test: bool | None = None
    validated_by: list[str] | None = None
    type: MovementType | None = None
    state: MovementState | None = None
    motive: MovementMotive | None = None
    note: str | None = None
    supplier: str | None = None
    reference: str | None = None
    movements: list[ArticleMovement] | None = None


class MovementCreation(BaseMovement):
    validated_by: list[str]
    type: MovementType
    state: MovementState
    movements: list[ArticleMovement]


class Movement(BaseTactillModel, BaseMovement):
    shop_id: TactillUUID
    number: int | None = None
