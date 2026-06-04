from pydantic import BaseModel

from tactill.entities.base import (
    BaseEntity,
    IconText,
    TactillColor,
    TactillName,
    TactillUUID,
)


class ArticleCreate(BaseModel):
    category_id: TactillUUID
    taxes: list[TactillUUID]
    name: TactillName
    icon_text: IconText
    color: TactillColor
    barcode: str | None = None
    in_stock: bool = True
    reference: str | None = None
    full_price: float


class ArticleUpdate(BaseModel):
    taxes: list[TactillUUID]
    name: TactillName | None = None
    icon_text: IconText | None = None
    color: TactillColor
    barcode: str | None = None
    reference: str | None = None
    full_price: float | None = None


class Article(BaseEntity):
    category_id: TactillUUID
    taxes: list[TactillUUID]
    name: TactillName
    icon_text: IconText
    color: TactillColor
    barcode: str | None = None
    in_stock: bool
    reference: str | None = None
    full_price: float | None = None
    stock_quantity: int | None = None
