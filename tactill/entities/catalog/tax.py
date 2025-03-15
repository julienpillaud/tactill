from pydantic import BaseModel

from tactill.entities.base import BaseTactillModel, TactillUUID


class TaxCreation(BaseModel):
    test: bool | None = None
    is_default: bool
    name: str
    in_price: bool
    rate: float


class TaxModification(BaseModel):
    test: bool | None = None
    is_default: bool | None = None
    name: str | None = None
    in_price: bool | None = None
    rate: float | None = None


class Tax(BaseTactillModel):
    company_id: TactillUUID

    test: bool | None = None
    is_default: bool | None = None
    name: str | None = None
    in_price: bool | None = None
    rate: float | None = None
