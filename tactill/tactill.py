import logging
from json import JSONDecodeError
from typing import Any

import httpx
from tenacity import (
    before_sleep_log,
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential_jitter,
)

from tactill import QueryParams
from tactill.entities import (
    Account,
    Article,
    ArticleCreation,
    ArticleModification,
    Category,
    CategoryCreation,
    CategoryModification,
    Movement,
    MovementCreation,
    TactillResponse,
    TactillUUID,
    Tax,
    TaxCreation,
    TaxModification,
)

logger = logging.getLogger(__name__)


class TactillError(Exception):
    def __init__(self, response: httpx.Response):
        super().__init__(response.text)

        self.error: Any = None
        try:
            error = response.json()
            self.error = TactillResponse.model_validate(error)
        except JSONDecodeError as json_decode_error:
            self.error = json_decode_error


class TactillClient:
    api_url = "https://api4.tactill.com/v1"

    def __init__(self, api_key: TactillUUID) -> None:
        self.headers = {"x-api-key": api_key}
        url = f"{self.api_url}/account/account"

        with httpx.Client(headers=self.headers, timeout=15) as client:
            response = client.get(url)

        if response.status_code != httpx.codes.OK:
            raise TactillError(response)

        account = response.json()
        self.account = Account.model_validate(account)
        self.node_id = self.account.nodes[0]
        self.company_id = self.account.companies[0]
        self.shop_id = self.account.shops[0]

    @retry(
        retry=retry_if_exception_type(httpx.ReadTimeout),
        wait=wait_exponential_jitter(),
        stop=stop_after_attempt(5),
        reraise=True,
        before_sleep=before_sleep_log(logger, logging.WARNING),
    )
    def _request(
        self,
        method: str,
        url: str,
        /,
        expected_status: httpx.codes,
        params: Any = None,
        json: Any = None,
    ) -> Any:
        with httpx.Client(headers=self.headers, timeout=15) as client:
            response = client.request(method=method, url=url, params=params, json=json)

        if response.status_code != expected_status:
            raise TactillError(response)

        return response.json()

    def _get(
        self,
        url: str,
        query: QueryParams,
        extra_params: dict[str, str] | None = None,
    ) -> Any:
        extra_params = extra_params or {}
        params = query.build(extra_params)
        return self._request("GET", url, expected_status=httpx.codes.OK, params=params)

    def _delete(self, url: str) -> TactillResponse:
        response = self._request("DELETE", url, expected_status=httpx.codes.OK)
        return TactillResponse.model_validate(response)

    def get_articles(self, query: QueryParams | None = None) -> list[Article]:
        query = query or QueryParams()
        response = self._get(
            url=f"{self.api_url}/catalog/articles",
            query=query,
            extra_params={"node_id": self.node_id},
        )
        return [Article.model_validate(entity) for entity in response]

    def create_article(self, article_creation: ArticleCreation) -> Article:
        article = article_creation.model_dump(exclude_none=True)
        article["node_id"] = self.node_id

        response = self._request(
            "POST",
            f"{self.api_url}/catalog/articles",
            expected_status=httpx.codes.CREATED,
            json=article,
        )
        return Article.model_validate(response)

    def delete_article(self, article_id: TactillUUID) -> TactillResponse:
        return self._delete(f"{self.api_url}/catalog/articles/{article_id}")

    def get_article(self, article_id: TactillUUID) -> Article:
        response = self._request(
            "GET",
            f"{self.api_url}/catalog/articles/{article_id}",
            expected_status=httpx.codes.OK,
        )
        return Article.model_validate(response)

    def update_article(
        self,
        article_id: TactillUUID,
        article_modification: ArticleModification,
    ) -> TactillResponse:
        article = article_modification.model_dump(exclude_none=True)

        response = self._request(
            "PUT",
            f"{self.api_url}/catalog/articles/{article_id}",
            expected_status=httpx.codes.OK,
            json=article,
        )
        return TactillResponse.model_validate(response)

    def get_categories(self, query: QueryParams | None = None) -> list[Category]:
        query = query or QueryParams()
        response = self._get(
            url=f"{self.api_url}/catalog/categories",
            query=query,
            extra_params={"company_id": self.company_id},
        )
        return [Category.model_validate(entity) for entity in response]

    def create_category(self, category_creation: CategoryCreation) -> Category:
        category = category_creation.model_dump(exclude_none=True)
        category["company_id"] = self.company_id

        response = self._request(
            "POST",
            f"{self.api_url}/catalog/categories",
            expected_status=httpx.codes.CREATED,
            json=category,
        )

        return Category.model_validate(response)

    def delete_category(self, category_id: TactillUUID) -> TactillResponse:
        return self._delete(f"{self.api_url}/catalog/categories/{category_id}")

    def get_category(self, category_id: TactillUUID) -> Category:
        response = self._request(
            "GET",
            f"{self.api_url}/catalog/categories/{category_id}",
            expected_status=httpx.codes.OK,
        )
        return Category.model_validate(response)

    def update_category(
        self,
        category_id: TactillUUID,
        category_modification: CategoryModification,
    ) -> TactillResponse:
        article = category_modification.model_dump(exclude_none=True)

        response = self._request(
            "PUT",
            f"{self.api_url}/catalog/categories/{category_id}",
            expected_status=httpx.codes.OK,
            json=article,
        )
        return TactillResponse.model_validate(response)

    def get_taxes(self, query: QueryParams | None = None) -> list[Tax]:
        query = query or QueryParams()
        response = self._get(
            url=f"{self.api_url}/catalog/taxes",
            query=query,
            extra_params={"company_id": self.company_id},
        )
        return [Tax.model_validate(entity) for entity in response]

    def create_tax(self, tax_creation: TaxCreation) -> Tax:
        tax = tax_creation.model_dump(exclude_none=True)
        tax["company_id"] = self.company_id

        response = self._request(
            "POST",
            f"{self.api_url}/catalog/taxes",
            expected_status=httpx.codes.CREATED,
            json=tax,
        )
        return Tax.model_validate(response)

    def delete_tax(self, tax_id: TactillUUID) -> TactillResponse:
        url = f"{self.api_url}/catalog/taxes/{tax_id}"
        return self._delete(url)

    def get_tax(self, tax_id: TactillUUID) -> Tax:
        response = self._request(
            "GET",
            f"{self.api_url}/catalog/taxes/{tax_id}",
            expected_status=httpx.codes.OK,
        )
        return Tax.model_validate(response)

    def update_tax(
        self,
        tax_id: TactillUUID,
        tax_modification: TaxModification,
    ) -> TactillResponse:
        url = f"{self.api_url}/catalog/taxes/{tax_id}"
        tax = tax_modification.model_dump(exclude_none=True)
        response = self._request("PUT", url, expected_status=httpx.codes.OK, json=tax)
        return TactillResponse.model_validate(response)

    def get_movements(self, query: QueryParams | None = None) -> list[Movement]:
        query = query or QueryParams()
        response = self._get(
            url=f"{self.api_url}/stock/movements",
            query=query,
            extra_params={"shop_id": self.shop_id},
        )
        return [Movement.model_validate(entity) for entity in response]

    def create_movement(self, movement_creation: MovementCreation) -> Movement:
        payload = movement_creation.model_dump(exclude_none=True)
        payload["shop_id"] = self.shop_id

        response = self._request(
            "POST",
            f"{self.api_url}/stock/movements",
            expected_status=httpx.codes.CREATED,
            json=payload,
        )
        return Movement.model_validate(response)
