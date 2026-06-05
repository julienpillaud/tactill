import typing

from tactill.entities.article import Article, ArticleCreate, ArticleUpdate
from tactill.entities.base import TactillUUID
from tactill.entities.response import TactillResponse
from tactill.filters import FilterEntity, FilterOperator
from tactill.mixin import ClientMixin

if typing.TYPE_CHECKING:
    from tactill.asynchronous.base import AsyncTactillClient


class AsyncArticlesResource(ClientMixin):
    def __init__(self, client: AsyncTactillClient) -> None:
        self.client = client
        self.base_url = f"{self.BASE_URL}/catalog/articles"

    async def get_all(
        self,
        limit: int = 100,
        skip: int = 0,
        filters: list[FilterEntity] | None = None,
        order: str | None = None,
    ) -> list[Article]:
        params = self._build_params(
            limit=limit,
            skip=skip,
            filters=filters,
            order=order,
            extra_params={"node_id": self.client.account.node_id},
        )
        response = await self.client.request("GET", self.base_url, params=params)
        return self._handle_validation(response, response_model=list[Article])

    async def get_by_category(
        self,
        category_id: TactillUUID,
        *,
        limit: int = 1000,
        in_stock: bool = False,
    ) -> list[Article]:
        articles = await self.get_all(
            limit=limit,
            filters=[
                FilterEntity(
                    field="category_id",
                    value=[category_id],
                    operator=FilterOperator.IN,
                )
            ],
        )
        if in_stock:
            return [
                article
                for article in articles
                if article.stock_quantity and article.stock_quantity > 0
            ]
        return articles

    async def get(self, article_id: TactillUUID) -> Article:
        response = await self.client.request("GET", f"{self.base_url}/{article_id}")
        return self._handle_validation(response, response_model=Article)

    async def create(self, data: ArticleCreate) -> Article:
        json = data.model_dump(exclude_none=True)
        json["node_id"] = self.client.account.node_id
        response = await self.client.request("POST", self.base_url, json=json)
        return self._handle_validation(response, response_model=Article)

    async def update(
        self,
        article_id: TactillUUID,
        data: ArticleUpdate,
    ) -> TactillResponse:
        json = data.model_dump(exclude_none=True)
        response = await self.client.request(
            "PUT",
            f"{self.base_url}/{article_id}",
            json=json,
        )
        return self._handle_validation(response, response_model=TactillResponse)
