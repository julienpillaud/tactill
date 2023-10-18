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
    deprecated: bool | None = None
    test: bool | None = None
    taxes: list[TactillUUID]
    no_price: bool | None = None
    full_price: float | None = None
    taxfree_price: float | None = None
    barcode: str | None = None
    reference: str | None = None
    weight: float | None = None
    in_stock: bool | None = None
    ignore_stock: bool | None = None
    buy_price: float | None = None
    variations: list[ArticleVariation] | None = None
    stock_quantity: float | None = None


class BaseArticle(BaseModel):
    test: bool | None = None
    category_id: TactillUUID | None = None
    discounts: list[TactillUUID] | None = None
    taxes: list[TactillUUID] | None = None
    name: str | None = None
    icon_text: str | None = None
    summary: str | None = None
    image: str | None = None
    color: TactillColor | None = None
    full_price: float | None = None
    taxfree_price: float | None = None
    barcode: str | None = None
    reference: str | None = None
    unit: ArticleUnit | None = None
    weight: float | None = None
    in_stock: bool | None = None
    ignore_stock: bool | None = None
    buy_price: float | None = None
    variations: list[ArticleVariationOptions] | None = None
    declinations: list[ArticleDeclination] | None = None
    options: list[TactillUUID] | None = None


class ArticleCreation(BaseArticle):
    category_id: TactillUUID
    taxes: list[TactillUUID]
    name: str


class ArticleModification(BaseArticle):
    taxes: list[TactillUUID]


class Article(BaseTactillModel, BaseArticle):
    node_id: TactillUUID
    taxes: list[TactillUUID]
    is_default: bool | None = None
    stock_quantity: int = 0
