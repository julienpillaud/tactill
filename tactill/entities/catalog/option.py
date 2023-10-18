from pydantic import BaseModel

from tactill.entities.base import BaseTactillModel, TactillUUID


class BaseOptionList(BaseModel):
    options: list[TactillUUID] | None = None
    name: str | None = None
    multiple: bool | None = None
    mandatory: bool | None = None


class OptionListCreation(BaseOptionList):
    options: list[TactillUUID]
    name: str
    multiple: bool
    mandatory: bool


class OptionListModification(BaseOptionList):
    options: list[TactillUUID]


class OptionList(BaseTactillModel, BaseOptionList):
    node_id: TactillUUID
    options: list[TactillUUID]


class BaseOption(BaseModel):
    test: bool | None = None
    name: str | None = None
    price: float | None = None


class OptionCreation(BaseOption):
    name: str
    price: float


class OptionModification(BaseOption):
    pass


class Option(BaseTactillModel, BaseOption):
    node_id: TactillUUID
