from typing import Literal

from pydantic import BaseModel

from tactill.entities.base import BaseTactillModel, TactillColor, TactillUUID

ArticleUnit = Literal["", "kg", "l", "m", "min"]


class ValuePair(BaseModel):
    priority: float
    value: str


class ArticleVariationOptions(BaseModel):
    key: str
    values: list[ValuePair]
    priority: float


class ArticleVariation(BaseModel):
    key: str
    value: str
    priority: float


class ArticleDeclination(BaseModel):
    id: str
    deprecated: bool = False
    test: bool = False
    taxes: list[TactillUUID]
    no_price: bool = False
    full_price: float | None = None
    taxfree_price: float | None = None
    barcode: str | None = None
    reference: str | None = None
    weight: float | None = None
    in_stock: bool = False
    ignore_stock: bool = True
    buy_price: float | None = None
    variations: list[ArticleVariation] | None = None
    stock_quantity: float | None = None


class Article(BaseTactillModel):
    test: bool = False
    node_id: TactillUUID
    category_id: TactillUUID | None = None
    discounts: list[TactillUUID] | None = None
    taxes: list[TactillUUID]
    is_default: bool = False
    name: str | None = None
    icon_text: str | None = None
    summary: str | None = None
    image: str = ""
    color: TactillColor = "#57DB47"
    full_price: float | None = None
    taxfree_price: float | None = None
    barcode: str | None = None
    reference: str | None = None
    unit: ArticleUnit = ""
    weight: float | None = None
    in_stock: bool = False
    ignore_stock: bool = True
    buy_price: float | None = None
    variations: list[ArticleVariationOptions] | None = None
    declinations: list[ArticleDeclination] | None = None
    options: list[TactillUUID] | None = None
    stock_quantity: float | None = None


class ArticleCreation(BaseModel):
    test: bool = False
    category_id: TactillUUID
    taxes: list[TactillUUID]
    name: str
    icon_text: str = ""
    summary: str = ""
    color: TactillColor = "#57DB47"
    full_price: float
    barcode: str = ""
    reference: str = ""
    in_stock: bool = False
    ignore_stock: bool = True
