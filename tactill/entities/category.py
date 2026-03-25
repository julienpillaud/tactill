from pydantic import BaseModel

from tactill.entities.base import BaseTactillModel, IconText, TactillColor, TactillName


class CategoryCreation(BaseModel):
    icon_text: IconText
    color: TactillColor = TactillColor.GREEN
    name: TactillName


class CategoryModification(BaseModel):
    icon_text: str | None = None
    color: TactillColor | None = None
    name: str | None = None


class Category(BaseTactillModel):
    icon_text: IconText
    color: TactillColor
    name: TactillName
