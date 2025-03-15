from pydantic import BaseModel

from tactill.entities.base import BaseTactillModel, TactillUUID


class OptionListCreation(BaseModel):
    options: list[TactillUUID]
    name: str
    multiple: bool
    mandatory: bool


class OptionListModification(BaseModel):
    options: list[TactillUUID]
    name: str | None = None
    multiple: bool | None = None
    mandatory: bool | None = None


class OptionList(BaseTactillModel):
    node_id: TactillUUID

    options: list[TactillUUID]
    name: str | None = None
    multiple: bool | None = None
    mandatory: bool | None = None


class OptionCreation(BaseModel):
    test: bool | None = None
    name: str
    price: float


class OptionModification(BaseModel):
    test: bool | None = None
    name: str | None = None
    price: float | None = None


class Option(BaseTactillModel):
    node_id: TactillUUID

    test: bool | None = None
    name: str | None = None
    price: float | None = None
