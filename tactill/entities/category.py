from tactill.entities.base import BaseTactillModel, TactillColor, TactillUUID


class Category(BaseTactillModel):
    test: bool = False
    company_id: TactillUUID
    is_default: bool = False
    image: str = ""
    color: TactillColor = "#57DB47"
    icon_text: str | None = None
    name: str | None = None
