from typing import cast

import httpx2

from tactill.entities.account import Account
from tactill.mixin import ClientMixin
from tactill.synchronous.articles import ArticlesResource
from tactill.synchronous.categories import CategoriesResource
from tactill.synchronous.movements import MovementsResource
from tactill.synchronous.taxes import TaxesResource
from tactill.types import JsonValue, QueryParams


class TactillClient(ClientMixin):
    def __init__(
        self,
        api_key: str,
        http_client: httpx2.Client,
        account: Account,
    ) -> None:
        self._http_client = http_client
        self.headers = {"x-api-key": api_key}
        self.account = account

        self.articles = ArticlesResource(self)
        self.categories = CategoriesResource(self)
        self.taxes = TaxesResource(self)
        self.movements = MovementsResource(self)

    @classmethod
    def create(cls, api_key: str, http_client: httpx2.Client) -> TactillClient:
        account = cls._get_account(api_key=api_key, http_client=http_client)
        return cls(api_key=api_key, http_client=http_client, account=account)

    @classmethod
    def _get_account(
        cls,
        api_key: str,
        http_client: httpx2.Client,
    ) -> Account:
        with cls._handle_response():
            response = http_client.get(
                f"{cls.BASE_URL}/account/account",
                headers={"x-api-key": api_key},
            )
            response.raise_for_status()
            result = response.json()

        return cls._handle_validation(result, response_model=Account)

    def request(
        self,
        method: str,
        url: str,
        *,
        params: QueryParams | None = None,
        json: JsonValue | None = None,
    ) -> JsonValue:
        with self._handle_response():
            response = self._http_client.request(
                method,
                url,
                params=params,
                json=json,
                headers=self.headers,
            )
            response.raise_for_status()
            return cast(JsonValue, response.json())
