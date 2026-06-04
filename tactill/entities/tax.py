from tactill.entities.base import BaseEntity, TactillName


class Tax(BaseEntity):
    name: TactillName
    rate: float
