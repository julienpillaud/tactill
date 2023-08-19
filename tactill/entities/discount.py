from datetime import datetime
from typing import Literal

from pydantic import BaseModel, field_serializer

from tactill.entities.base import BaseTactillModel, TactillColor, TactillUUID


class DiscountCreation(BaseModel):
    test: bool | None = None
    name: str
    rate: float | None = None
    type: Literal["numeric", "rate"] | None = None
    start_date: datetime | None = None
    end_date: datetime | None = None
    barcode: str | None = None
    icon_text: str | None = None
    color: TactillColor | None = None

    @field_serializer("start_date")
    def serialize_start_date(self, date: datetime | None) -> str | None:
        return date.isoformat() if date else None

    @field_serializer("end_date")
    def serialize_end_date(self, date: datetime | None) -> str | None:
        return date.isoformat() if date else None


class Discount(BaseTactillModel, DiscountCreation):
    shop_id: TactillUUID
