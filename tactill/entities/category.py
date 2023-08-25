from pydantic import BaseModel

from tactill.entities.base import BaseTactillModel, TactillColor, TactillUUID


class BaseCategory(BaseModel):
    test: bool | None = None
    image: str | None = None
    color: TactillColor | None = None
    icon_text: str | None = None
    name: str | None = None


class CategoryCreation(BaseCategory):
    name: str


class CategoryModification(BaseCategory):
    pass


class Category(BaseTactillModel, BaseCategory):
    company_id: TactillUUID
    is_default: bool | None = None
