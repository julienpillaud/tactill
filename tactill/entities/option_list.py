from pydantic import BaseModel

from tactill.entities.base import BaseTactillModel, TactillUUID


class OptionListCreation(BaseModel):
    options: list[TactillUUID] | None = None
    name: str
    multiple: bool
    mandatory: bool


class OptionList(BaseTactillModel, OptionListCreation):
    node_id: TactillUUID
