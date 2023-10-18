from pydantic import BaseModel

from tactill.entities.base import BaseTactillModel, TactillUUID


class BasePack(BaseModel):
    articles: list[TactillUUID] | None = None
    full_price: float | None = None
    taxfree_price: float | None = None
    taxes: list[TactillUUID] | None = None
    discounts: list[TactillUUID] | None = None


class PackCreation(BasePack):
    articles: list[TactillUUID]
    taxes: list[TactillUUID]
    discounts: list[TactillUUID]


class PackModification(BasePack):
    articles: list[TactillUUID]
    taxes: list[TactillUUID]
    discounts: list[TactillUUID]


class Pack(BaseTactillModel, BasePack):
    node_id: TactillUUID
    articles: list[TactillUUID]
    taxes: list[TactillUUID]
    discounts: list[TactillUUID]
