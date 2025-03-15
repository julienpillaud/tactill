from pydantic import BaseModel

from tactill.entities.base import BaseTactillModel, TactillColor, TactillUUID


class BaseCategory(BaseModel):
    test: bool | None = None
    image: str | None = None
    color: TactillColor | None = None
    icon_text: str | None = None
    name: str | None = None


class CategoryCreation(BaseModel):
    test: bool | None = None
    image: str | None = None
    color: TactillColor | None = None
    icon_text: str | None = None
    name: str


class CategoryModification(BaseModel):
    test: bool | None = None
    image: str | None = None
    color: TactillColor | None = None
    icon_text: str | None = None
    name: str | None = None


class Category(BaseTactillModel):
    company_id: TactillUUID
    is_default: bool | None = None

    test: bool | None = None
    image: str | None = None
    color: TactillColor | None = None
    icon_text: str | None = None
    name: str | None = None
