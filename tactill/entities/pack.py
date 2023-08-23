from pydantic import BaseModel

from tactill.entities.base import BaseTactillModel, TactillUUID


class PackCreation(BaseModel):
    articles: list[TactillUUID]
    full_price: float | None = None
    taxfree_price: float | None = None
    taxes: list[TactillUUID]
    discounts: list[TactillUUID]


class Pack(BaseTactillModel, PackCreation):
    node_id: TactillUUID
