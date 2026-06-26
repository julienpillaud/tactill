import asyncio
from typing import cast

import httpx

from tactill.asynchronous.articles import AsyncArticlesResource
from tactill.asynchronous.categories import AsyncCategoriesResource
from tactill.asynchronous.movements import AsyncMovementsResource
from tactill.asynchronous.taxes import AsyncTaxesResource
from tactill.mixin import ClientMixin
from tactill.types import JsonValue, QueryParams


class AsyncTactillClient(ClientMixin):
    def __init__(
        self,
        api_key: str,
        http_client: httpx.AsyncClient,
        max_concurrency: int = 100,
    ) -> None:
        self._http_client = http_client
        self._semaphore = asyncio.Semaphore(max_concurrency)
        self.headers = {"x-api-key": api_key}
        self.account = self._get_account(headers=self.headers)

        self.articles = AsyncArticlesResource(self)
        self.categories = AsyncCategoriesResource(self)
        self.taxes = AsyncTaxesResource(self)
        self.movements = AsyncMovementsResource(self)

    async def request(
        self,
        method: str,
        url: str,
        *,
        params: QueryParams | None = None,
        json: JsonValue | None = None,
    ) -> JsonValue:
        async with self._semaphore:
            with self._handle_response():
                response = await self._http_client.request(
                    method,
                    url,
                    params=params,
                    json=json,
                    headers=self.headers,
                )
                response.raise_for_status()
                return cast(JsonValue, response.json())
