import asyncio
from typing import cast

import httpx2

from tactill.asynchronous.articles import AsyncArticlesResource
from tactill.asynchronous.categories import AsyncCategoriesResource
from tactill.asynchronous.movements import AsyncMovementsResource
from tactill.asynchronous.taxes import AsyncTaxesResource
from tactill.entities.account import Account
from tactill.mixin import ClientMixin
from tactill.types import JsonValue, QueryParams


class AsyncTactillClient(ClientMixin):
    def __init__(
        self,
        api_key: str,
        http_client: httpx2.AsyncClient,
        account: Account,
        max_concurrency: int = 10,
    ) -> None:
        self._http_client = http_client
        self._semaphore = asyncio.Semaphore(max_concurrency)
        self.headers = {"x-api-key": api_key}
        self.account = account

        self.articles = AsyncArticlesResource(self)
        self.categories = AsyncCategoriesResource(self)
        self.taxes = AsyncTaxesResource(self)
        self.movements = AsyncMovementsResource(self)

    @classmethod
    async def create(
        cls,
        api_key: str,
        http_client: httpx2.AsyncClient,
        max_concurrency: int = 10,
    ) -> AsyncTactillClient:
        account = await cls._get_account(api_key=api_key, http_client=http_client)
        return cls(
            api_key=api_key,
            http_client=http_client,
            account=account,
            max_concurrency=max_concurrency,
        )

    @classmethod
    async def _get_account(
        cls,
        api_key: str,
        http_client: httpx2.AsyncClient,
    ) -> Account:
        with cls._handle_response():
            response = await http_client.get(
                f"{cls.BASE_URL}/account/account",
                headers={"x-api-key": api_key},
            )
            response.raise_for_status()
            result = response.json()

        return cls._handle_validation(result, response_model=Account)

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
