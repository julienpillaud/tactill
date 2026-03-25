from pydantic import BaseModel

from tactill.entities.base import BaseTactillModel, TactillName


class TaxCreation(BaseModel):
    name: TactillName
    rate: float


class TaxModification(BaseModel):
    name: TactillName | None = None
    rate: float | None = None


class Tax(BaseTactillModel):
    name: TactillName
    rate: float
