import typing

from tactill.entities.base import TactillUUID
from tactill.entities.category import Category, CategoryCreate, CategoryUpdate
from tactill.entities.response import TactillResponse
from tactill.filters import FilterEntity
from tactill.mixin import ClientMixin

if typing.TYPE_CHECKING:
    from tactill.asynchronous.base import AsyncTactillClient


class AsyncCategoriesResource(ClientMixin):
    def __init__(self, client: AsyncTactillClient) -> None:
        self.client = client
        self.base_url = f"{self.BASE_URL}/catalog/categories"

    async def get_all(
        self,
        limit: int = 100,
        skip: int = 0,
        filters: list[FilterEntity] | None = None,
        order: str | None = None,
    ) -> list[Category]:
        params = self._build_params(
            limit=limit,
            skip=skip,
            filters=filters,
            order=order,
            extra_params={"company_id": self.client.account.company_id},
        )
        response = await self.client.request("GET", self.base_url, params=params)
        return self._handle_validation(response, response_model=list[Category])

    async def get(self, category_id: TactillUUID) -> Category:
        response = await self.client.request("GET", f"{self.base_url}/{category_id}")
        return self._handle_validation(response, response_model=Category)

    async def create(self, data: CategoryCreate) -> Category:
        json = data.model_dump(exclude_none=True)
        json["company_id"] = self.client.account.company_id
        response = await self.client.request("POST", self.base_url, json=json)
        return self._handle_validation(response, response_model=Category)

    async def update(
        self,
        category_id: TactillUUID,
        data: CategoryUpdate,
    ) -> TactillResponse:
        json = data.model_dump(exclude_unset=True)
        response = await self.client.request(
            "PUT",
            f"{self.base_url}/{category_id}",
            json=json,
        )
        return self._handle_validation(response, response_model=TactillResponse)
