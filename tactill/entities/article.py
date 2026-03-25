from pydantic import BaseModel

from tactill.entities.base import (
    BaseTactillModel,
    IconText,
    TactillColor,
    TactillName,
    TactillUUID,
)


class ArticleCreation(BaseModel):
    category_id: TactillUUID
    taxes: list[TactillUUID]
    name: TactillName
    icon_text: IconText
    color: TactillColor = TactillColor.GREEN
    barcode: str = ""
    in_stock: bool = True
    reference: str | None = None
    full_price: float


class ArticleModification(BaseModel):
    category_id: TactillUUID | None = None
    taxes: list[TactillUUID]
    name: TactillName | None = None
    icon_text: IconText | None = None
    # color not mandatory for the API but if not provided, it will be reset
    color: TactillColor
    barcode: str | None = None
    # in_stock not mandatory for the API but if not provided, it will be reset
    in_stock: bool
    reference: str | None = None
    full_price: float | None = None


class Article(BaseTactillModel):
    category_id: TactillUUID
    taxes: list[TactillUUID]
    name: TactillName
    icon_text: IconText
    color: TactillColor
    barcode: str = ""
    in_stock: bool
    reference: str | None = None
    full_price: float | None = None
    stock_quantity: int | None = None
