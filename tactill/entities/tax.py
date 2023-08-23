from pydantic import BaseModel

from tactill.entities.base import BaseTactillModel, TactillUUID


class TaxCreation(BaseModel):
    test: bool | None = None
    is_default: bool
    name: str
    in_price: bool
    rate: float


class Tax(BaseTactillModel, TaxCreation):
    company_id: TactillUUID
