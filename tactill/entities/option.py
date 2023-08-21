from pydantic import BaseModel

from tactill.entities.base import BaseTactillModel, TactillUUID


class OptionCreation(BaseModel):
    test: bool | None = None
    name: str
    price: float


class Option(BaseTactillModel, OptionCreation):
    node_id: TactillUUID


class OptionListCreation(BaseModel):
    options: list[TactillUUID]
    name: str
    multiple: bool
    mandatory: bool


class OptionList(BaseTactillModel, OptionListCreation):
    node_id: TactillUUID
