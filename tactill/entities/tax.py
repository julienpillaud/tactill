from pydantic import BaseModel

from tactill.entities.base import BaseTactillModel, TactillUUID


class BaseTax(BaseModel):
    test: bool | None = None
    is_default: bool | None = None
    name: str | None = None
    in_price: bool | None = None
    rate: float | None = None


class TaxCreation(BaseTax):
    is_default: bool
    name: str
    in_price: bool
    rate: float


class TaxModification(BaseTax):
    pass


class Tax(BaseTactillModel, BaseTax):
    company_id: TactillUUID
