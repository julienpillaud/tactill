from datetime import datetime
from typing import Literal

from tactill.entities.base import BaseTactillModel, TactillColor, TactillUUID

DiscountType = Literal["numeric", "rate"]


class Discount(BaseTactillModel):
    test: bool = False
    shop_id: TactillUUID
    name: str | None = None
    rate: float | None = None
    type: DiscountType | None = None
    start_date: datetime | None = None
    end_date: datetime | None = None
    barcode: str | None = None
    icon_text: str | None = None
    color: TactillColor = "#57DB47"
