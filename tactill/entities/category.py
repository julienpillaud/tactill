from pydantic import BaseModel

from tactill.entities.base import BaseTactillModel, TactillColor, TactillUUID


class CategoryCreation(BaseModel):
    test: bool | None = None
    image: str | None = None
    color: TactillColor | None = None
    icon_text: str | None = None
    name: str


class Category(BaseTactillModel, CategoryCreation):
    company_id: TactillUUID
    is_default: bool = False
