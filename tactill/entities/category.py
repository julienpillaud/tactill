from pydantic import BaseModel

from tactill.entities.base import BaseEntity, IconText, TactillColor, TactillName


class CategoryCreate(BaseModel):
    name: TactillName
    icon_text: IconText
    color: TactillColor


class CategoryUpdate(BaseModel):
    name: TactillName | None = None
    icon_text: IconText | None = None
    color: TactillColor


class Category(BaseEntity):
    name: TactillName
    icon_text: IconText
    color: TactillColor
