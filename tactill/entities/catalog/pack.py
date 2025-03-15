from pydantic import BaseModel

from tactill.entities.base import BaseTactillModel, TactillUUID


class PackCreation(BaseModel):
    articles: list[TactillUUID]
    full_price: float | None = None
    taxfree_price: float | None = None
    taxes: list[TactillUUID]
    discounts: list[TactillUUID]


class PackModification(BaseModel):
    articles: list[TactillUUID]
    full_price: float | None = None
    taxfree_price: float | None = None
    taxes: list[TactillUUID]
    discounts: list[TactillUUID]


class Pack(BaseTactillModel):
    node_id: TactillUUID

    articles: list[TactillUUID]
    full_price: float | None = None
    taxfree_price: float | None = None
    taxes: list[TactillUUID]
    discounts: list[TactillUUID]
