from tactill.entities.base import BaseTactillModel, TactillUUID


class Stock(BaseTactillModel):
    test: bool | None = None
    article_id: TactillUUID
    shop_id: TactillUUID
    declination_id: str | None = None
    buy_price: float | None = None
    units: int | None = None
    locked: bool | None = None
