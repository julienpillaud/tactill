import typing

from tactill.entities.base import TactillUUID
from tactill.entities.tax import Tax
from tactill.filters import FilterEntity
from tactill.mixin import ClientMixin

if typing.TYPE_CHECKING:
    from tactill.asynchronous.base import AsyncTactillClient


class AsyncTaxesResource(ClientMixin):
    def __init__(self, client: AsyncTactillClient) -> None:
        self.client = client
        self.base_url = f"{self.BASE_URL}/catalog/taxes"

    async def get_all(
        self,
        limit: int = 100,
        skip: int = 0,
        filters: list[FilterEntity] | None = None,
        order: str | None = None,
    ) -> list[Tax]:
        params = self._build_params(
            limit=limit,
            skip=skip,
            filters=filters,
            order=order,
            extra_params={"company_id": self.client.account.company_id},
        )
        response = await self.client.request("GET", self.base_url, params=params)
        return self._handle_validation(response, response_model=list[Tax])

    async def get(self, tax_id: TactillUUID) -> Tax:
        response = await self.client.request("GET", f"{self.base_url}/{tax_id}")
        return self._handle_validation(response, response_model=Tax)
