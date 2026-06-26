import typing

from tactill.entities.movement import Movement, MovementCreate
from tactill.filters import FilterEntity
from tactill.mixin import ClientMixin

if typing.TYPE_CHECKING:
    from tactill.asynchronous.base import AsyncTactillClient


class AsyncMovementsResource(ClientMixin):
    def __init__(self, client: AsyncTactillClient) -> None:
        self.client = client
        self.base_url = f"{self.BASE_URL}/stock/movements"

    async def get_all(
        self,
        limit: int = 100,
        skip: int = 0,
        filters: list[FilterEntity] | None = None,
        order: str | None = None,
        deprecated: bool = False,
    ) -> list[Movement]:
        params = self._build_params(
            limit=limit,
            skip=skip,
            filters=filters,
            order=order,
            deprecated=deprecated,
            extra_params={"shop_id": self.client.account.shop_id},
        )
        response = await self.client.request("GET", self.base_url, params=params)
        return self._handle_validation(response, response_model=list[Movement])

    async def create(self, data: MovementCreate) -> Movement:
        json = data.model_dump(mode="json", exclude_none=True)
        json["shop_id"] = self.client.account.shop_id
        response = await self.client.request("POST", self.base_url, json=json)
        return self._handle_validation(response, response_model=Movement)
