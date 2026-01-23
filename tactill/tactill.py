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
from tactill.entities.account.account import Account
from tactill.entities.base import TactillResponse, TactillUUID
from tactill.entities.catalog.article import (
    Article,
    ArticleCreation,
    ArticleModification,
)
from tactill.entities.catalog.category import (
    Category,
    CategoryCreation,
    CategoryModification,
)
from tactill.entities.catalog.discount import (
    Discount,
    DiscountCreation,
    DiscountModification,
)
from tactill.entities.catalog.option import (
    Option,
    OptionCreation,
    OptionList,
    OptionListCreation,
    OptionListModification,
    OptionModification,
)
from tactill.entities.catalog.pack import Pack, PackCreation, PackModification
from tactill.entities.catalog.tax import Tax, TaxCreation, TaxModification
from tactill.entities.stock.movement import Movement, MovementCreation

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
        url = f"{self.api_url}/catalog/articles"
        article = article_creation.model_dump(exclude_none=True)
        article["node_id"] = self.node_id

        response = self._request(
            "POST", url, expected_status=httpx.codes.CREATED, json=article
        )

        return Article.model_validate(response)

    def delete_article(self, article_id: TactillUUID) -> TactillResponse:
        url = f"{self.api_url}/catalog/articles/{article_id}"
        return self._delete(url)

    def get_article(self, article_id: TactillUUID) -> Article:
        url = f"{self.api_url}/catalog/articles/{article_id}"
        response = self._request("GET", url, expected_status=httpx.codes.OK)
        return Article.model_validate(response)

    def update_article(
        self,
        article_id: TactillUUID,
        article_modification: ArticleModification,
    ) -> TactillResponse:
        url = f"{self.api_url}/catalog/articles/{article_id}"
        article = article_modification.model_dump(exclude_none=True)
        response = self._request(
            "PUT", url, expected_status=httpx.codes.OK, json=article
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
        url = f"{self.api_url}/catalog/categories"
        category = category_creation.model_dump(exclude_none=True)
        category["company_id"] = self.company_id

        response = self._request(
            "POST", url, expected_status=httpx.codes.CREATED, json=category
        )

        return Category.model_validate(response)

    def delete_category(self, category_id: TactillUUID) -> TactillResponse:
        url = f"{self.api_url}/catalog/categories/{category_id}"
        return self._delete(url)

    def get_category(self, category_id: TactillUUID) -> Category:
        url = f"{self.api_url}/catalog/categories/{category_id}"
        response = self._request("GET", url, expected_status=httpx.codes.OK)
        return Category.model_validate(response)

    def update_category(
        self,
        category_id: TactillUUID,
        category_modification: CategoryModification,
    ) -> TactillResponse:
        url = f"{self.api_url}/catalog/categories/{category_id}"
        article = category_modification.model_dump(exclude_none=True)
        response = self._request(
            "PUT", url, expected_status=httpx.codes.OK, json=article
        )
        return TactillResponse.model_validate(response)

    def get_discounts(self, query: QueryParams | None = None) -> list[Discount]:
        query = query or QueryParams()
        response = self._get(
            url=f"{self.api_url}/catalog/discounts",
            query=query,
            extra_params={"shop_id": self.shop_id},
        )
        return [Discount.model_validate(entity) for entity in response]

    def create_discount(self, discount_creation: DiscountCreation) -> Discount:
        url = f"{self.api_url}/catalog/discounts"
        category = discount_creation.model_dump(exclude_none=True)
        category["shop_id"] = self.shop_id

        response = self._request(
            "POST", url, expected_status=httpx.codes.CREATED, json=category
        )

        return Discount.model_validate(response)

    def delete_discount(self, discount_id: TactillUUID) -> TactillResponse:
        url = f"{self.api_url}/catalog/discounts/{discount_id}"
        return self._delete(url)

    def get_discount(self, discount_id: TactillUUID) -> Discount:
        url = f"{self.api_url}/catalog/discounts/{discount_id}"
        response = self._request("GET", url, expected_status=httpx.codes.OK)
        return Discount.model_validate(response)

    def update_discount(
        self,
        discount_id: TactillUUID,
        discount_modification: DiscountModification,
    ) -> TactillResponse:
        url = f"{self.api_url}/catalog/discounts/{discount_id}"
        discount = discount_modification.model_dump(exclude_none=True)
        response = self._request(
            "PUT", url, expected_status=httpx.codes.OK, json=discount
        )
        return TactillResponse.model_validate(response)

    def get_option_lists(self, query: QueryParams | None = None) -> list[OptionList]:
        query = query or QueryParams()
        response = self._get(
            url=f"{self.api_url}/catalog/option_lists",
            query=query,
            extra_params={"node_id": self.node_id},
        )
        return [OptionList.model_validate(entity) for entity in response]

    def create_option_list(
        self,
        option_list_creation: OptionListCreation,
    ) -> OptionList:
        url = f"{self.api_url}/catalog/option_lists"
        option_list = option_list_creation.model_dump(exclude_none=True)
        option_list["node_id"] = self.node_id

        response = self._request(
            "POST", url, expected_status=httpx.codes.CREATED, json=option_list
        )

        return OptionList.model_validate(response)

    def delete_option_list(self, option_list_id: TactillUUID) -> TactillResponse:
        url = f"{self.api_url}/catalog/option_lists/{option_list_id}"
        return self._delete(url)

    def get_option_list(self, option_list_id: TactillUUID) -> OptionList:
        url = f"{self.api_url}/catalog/option_lists/{option_list_id}"
        response = self._request("GET", url, expected_status=httpx.codes.OK)
        return OptionList.model_validate(response)

    def update_option_list(
        self,
        option_list_id: TactillUUID,
        option_list_modification: OptionListModification,
    ) -> TactillResponse:
        url = f"{self.api_url}/catalog/option_lists/{option_list_id}"
        option_list = option_list_modification.model_dump(exclude_none=True)
        response = self._request(
            "PUT", url, expected_status=httpx.codes.OK, json=option_list
        )
        return TactillResponse.model_validate(response)

    def get_options(self, query: QueryParams | None = None) -> list[Option]:
        query = query or QueryParams()
        response = self._get(
            url=f"{self.api_url}/catalog/options",
            query=query,
            extra_params={"node_id": self.node_id},
        )
        return [Option.model_validate(entity) for entity in response]

    def create_option(self, option_creation: OptionCreation) -> Option:
        url = f"{self.api_url}/catalog/options"
        option = option_creation.model_dump(exclude_none=True)
        option["node_id"] = self.node_id

        response = self._request(
            "POST", url, expected_status=httpx.codes.CREATED, json=option
        )

        return Option.model_validate(response)

    def delete_option(self, option_id: TactillUUID) -> TactillResponse:
        url = f"{self.api_url}/catalog/options/{option_id}"
        return self._delete(url)

    def get_option(self, option_id: TactillUUID) -> Option:
        url = f"{self.api_url}/catalog/options/{option_id}"
        response = self._request("GET", url, expected_status=httpx.codes.OK)
        return Option.model_validate(response)

    def update_option(
        self,
        option_id: TactillUUID,
        option_modification: OptionModification,
    ) -> TactillResponse:
        url = f"{self.api_url}/catalog/options/{option_id}"
        option = option_modification.model_dump(exclude_none=True)
        response = self._request(
            "PUT", url, expected_status=httpx.codes.OK, json=option
        )
        return TactillResponse.model_validate(response)

    def get_packs(self, query: QueryParams | None = None) -> list[Pack]:
        query = query or QueryParams()
        response = self._get(
            url=f"{self.api_url}/catalog/packs",
            query=query,
            extra_params={"node_id": self.node_id},
        )
        return [Pack.model_validate(entity) for entity in response]

    def create_pack(self, pack_creation: PackCreation) -> Pack:
        url = f"{self.api_url}/catalog/packs"
        pack = pack_creation.model_dump(exclude_none=True)
        pack["node_id"] = self.node_id

        response = self._request(
            "POST", url, expected_status=httpx.codes.CREATED, json=pack
        )

        return Pack.model_validate(response)

    def delete_pack(self, pack_id: TactillUUID) -> TactillResponse:
        url = f"{self.api_url}/catalog/packs/{pack_id}"
        return self._delete(url)

    def get_pack(self, pack_id: TactillUUID) -> Pack:
        url = f"{self.api_url}/catalog/packs/{pack_id}"
        response = self._request("GET", url, expected_status=httpx.codes.OK)
        return Pack.model_validate(response)

    def update_pack(
        self,
        pack_id: TactillUUID,
        pack_modification: PackModification,
    ) -> TactillResponse:
        url = f"{self.api_url}/catalog/packs/{pack_id}"
        pack = pack_modification.model_dump(exclude_none=True)
        response = self._request("PUT", url, expected_status=httpx.codes.OK, json=pack)
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
        url = f"{self.api_url}/catalog/taxes"
        tax = tax_creation.model_dump(exclude_none=True)
        tax["company_id"] = self.company_id

        response = self._request(
            "POST", url, expected_status=httpx.codes.CREATED, json=tax
        )

        return Tax.model_validate(response)

    def delete_tax(self, tax_id: TactillUUID) -> TactillResponse:
        url = f"{self.api_url}/catalog/taxes/{tax_id}"
        return self._delete(url)

    def get_tax(self, tax_id: TactillUUID) -> Tax:
        url = f"{self.api_url}/catalog/taxes/{tax_id}"
        response = self._request("GET", url, expected_status=httpx.codes.OK)
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
        url = f"{self.api_url}/stock/movements"
        pack = movement_creation.model_dump(exclude_none=True)
        pack["shop_id"] = self.shop_id

        response = self._request(
            "POST", url, expected_status=httpx.codes.CREATED, json=pack
        )

        return Movement.model_validate(response)
