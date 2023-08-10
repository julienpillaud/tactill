from typing import Literal

from pydantic import BaseModel

from tactill.entities.base import BaseTactillModel, TactillUUID

ArticleColor = Literal[
    "#57DB47",
    "#6868DC",
    "#30BEA5",
    "#F44F60",
    "#1E8CFF",
    "#F2BA43",
    "#B455C8",
    "#FF6347",
    "#A06E58",
    "#9EA09E",
]
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
    original_id: str | None = None
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
    color: ArticleColor = "#57DB47"
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
    color: ArticleColor = "#57DB47"
    full_price: float
    barcode: str = ""
    reference: str = ""
    in_stock: bool = False
    ignore_stock: bool = True
