from json import JSONDecodeError
from typing import Any

import httpx

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

API_URL = "https://api4.tactill.com/v1"


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
    def __init__(self, api_key: TactillUUID) -> None:
        self.headers = {"x-api-key": api_key}
        url = f"{API_URL}/account/account"

        with httpx.Client(headers=self.headers, timeout=15) as client:
            response = client.get(url)

        if response.status_code != httpx.codes.OK:
            raise TactillError(response)

        account = response.json()
        self.account = Account.model_validate(account)
        self.node_id = self.account.nodes[0]
        self.company_id = self.account.companies[0]
        self.shop_id = self.account.shops[0]

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
        param: dict[str, str],
        limit: int = 100,
        skip: int = 0,
        filter: str | None = None,
        order: str | None = None,
    ) -> Any:
        params = param | {"limit": limit}
        if skip:
            params["skip"] = skip
        if filter:
            params["filter"] = filter
        if order:
            params["order"] = order

        return self._request("GET", url, expected_status=httpx.codes.OK, params=params)

    def _delete(self, url: str) -> TactillResponse:
        response = self._request("DELETE", url, expected_status=httpx.codes.OK)
        return TactillResponse.model_validate(response)

    def get_articles(
        self,
        limit: int = 100,
        skip: int = 0,
        filter: str | None = None,
        order: str | None = None,
    ) -> list[Article]:
        """
        Get a list of Article based on the given filters.

        :param limit: Limit the number of returned records.
        :param skip: Define an offset in the returned records.
        :param filter: Allow filtering the results based on query language.
        :param order: Allow ordering by field (example "field1=ASC&field2=DESC").

        :return: A list of retrieved Articles.
        """
        url = f"{API_URL}/catalog/articles"
        param = {"node_id": self.node_id}
        response = self._get(url, param, limit, skip, filter, order)
        return [Article.model_validate(entity) for entity in response]

    def create_article(self, article_creation: ArticleCreation) -> Article:
        """
        Create a new Article.

        :param article_creation: The Article creation data.

        :return: The created Article.
        """
        url = f"{API_URL}/catalog/articles"
        article = article_creation.model_dump(exclude_none=True)
        article["node_id"] = self.node_id

        response = self._request(
            "POST", url, expected_status=httpx.codes.CREATED, json=article
        )

        return Article.model_validate(response)

    def delete_article(self, article_id: TactillUUID) -> TactillResponse:
        """
        Delete an Article.

        :param article_id: The unique id of the article to be deleted.

        :return: A `TactillResponse` object representing the response from the API.
        """
        url = f"{API_URL}/catalog/articles/{article_id}"
        return self._delete(url)

    def get_article(self, article_id: TactillUUID) -> Article:
        """
        Get an Article by its unique id.

        :param article_id: The unique id of the Article.

        :return: The Article object with the corresponding id.
        """
        url = f"{API_URL}/catalog/articles/{article_id}"
        response = self._request("GET", url, expected_status=httpx.codes.OK)
        return Article.model_validate(response)

    def update_article(
        self, article_id: TactillUUID, article_modification: ArticleModification
    ) -> TactillResponse:
        """
        Modify an Article.

        :param article_id: The unique id of the Article.
        :param article_modification: The Article modification data.

        :return: A `TactillResponse` object representing the response from the API.
        """
        url = f"{API_URL}/catalog/articles/{article_id}"
        article = article_modification.model_dump(exclude_none=True)
        response = self._request(
            "PUT", url, expected_status=httpx.codes.OK, json=article
        )
        return TactillResponse.model_validate(response)

    def get_categories(
        self,
        limit: int = 100,
        skip: int = 0,
        filter: str | None = None,
        order: str | None = None,
    ) -> list[Category]:
        """
        Get a list of Category based on the given filters.

        :param limit: Limit the number of returned records.
        :param skip: Define an offset in the returned records.
        :param filter: Allow filtering the results based on query language.
        :param order: Allow ordering by field (example "field1=ASC&field2=DESC").

        :return: A list of retrieved Categories.
        """
        url = f"{API_URL}/catalog/categories"
        param = {"company_id": self.company_id}
        response = self._get(url, param, limit, skip, filter, order)
        return [Category.model_validate(entity) for entity in response]

    def create_category(self, category_creation: CategoryCreation) -> Category:
        """
        Create a new Category.

        :param category_creation: The Category creation data.

        :return: The created Category.
        """
        url = f"{API_URL}/catalog/categories"
        category = category_creation.model_dump(exclude_none=True)
        category["company_id"] = self.company_id

        response = self._request(
            "POST", url, expected_status=httpx.codes.CREATED, json=category
        )

        return Category.model_validate(response)

    def delete_category(self, category_id: TactillUUID) -> TactillResponse:
        """
        Delete a Category.

        :param category_id: The unique id of the category to be deleted.

        :return: A `TactillResponse` object representing the response from the API.
        """
        url = f"{API_URL}/catalog/categories/{category_id}"
        return self._delete(url)

    def get_category(self, category_id: TactillUUID) -> Category:
        """
        Get a Category by its unique id

        :param category_id: The unique id of the category.

        :return: The Category object with the corresponding id.
        """
        url = f"{API_URL}/catalog/categories/{category_id}"
        response = self._request("GET", url, expected_status=httpx.codes.OK)
        return Category.model_validate(response)

    def update_category(
        self, category_id: TactillUUID, category_modification: CategoryModification
    ) -> TactillResponse:
        """
        Modify a Category.

        :param category_id: The unique id of the Category.
        :param category_modification: The Category modification data.

        :return: A `TactillResponse` object representing the response from the API.
        """
        url = f"{API_URL}/catalog/categories/{category_id}"
        article = category_modification.model_dump(exclude_none=True)
        response = self._request(
            "PUT", url, expected_status=httpx.codes.OK, json=article
        )
        return TactillResponse.model_validate(response)

    def get_discounts(
        self,
        limit: int = 100,
        skip: int = 0,
        filter: str | None = None,
        order: str | None = None,
    ) -> list[Discount]:
        """
        Get a list of Discount based on the given filters.

        :param limit: Limit the number of returned records.
        :param skip: Define an offset in the returned records.
        :param filter: Allow filtering the results based on query language.
        :param order: Allow ordering by field (example "field1=ASC&field2=DESC").

        :return: A list of retrieved Discounts.
        """
        url = f"{API_URL}/catalog/discounts"
        param = {"shop_id": self.shop_id}
        response = self._get(url, param, limit, skip, filter, order)
        return [Discount.model_validate(entity) for entity in response]

    def create_discount(self, discount_creation: DiscountCreation) -> Discount:
        """
        Create a new Discount.

        :param discount_creation: The Discount creation data.

        :return: The created Discount.
        """
        url = f"{API_URL}/catalog/discounts"
        category = discount_creation.model_dump(exclude_none=True)
        category["shop_id"] = self.shop_id

        response = self._request(
            "POST", url, expected_status=httpx.codes.CREATED, json=category
        )

        return Discount.model_validate(response)

    def delete_discount(self, discount_id: TactillUUID) -> TactillResponse:
        """
        Delete a Discount.

        :param discount_id: The unique id of the discount to be deleted.

        :return: A `TactillResponse` object representing the response from the API.
        """
        url = f"{API_URL}/catalog/discounts/{discount_id}"
        return self._delete(url)

    def get_discount(self, discount_id: TactillUUID) -> Discount:
        """
        Get a Discount by its unique id

        :param discount_id: The unique id of the discount.

        :return: The Discount object with the corresponding id.
        """
        url = f"{API_URL}/catalog/discounts/{discount_id}"
        response = self._request("GET", url, expected_status=httpx.codes.OK)
        return Discount.model_validate(response)

    def update_discount(
        self, discount_id: TactillUUID, discount_modification: DiscountModification
    ) -> TactillResponse:
        """
        Modify a Discount.

        :param discount_id: The unique id of the Discount.
        :param discount_modification: The Discount modification data.

        :return: A `TactillResponse` object representing the response from the API.
        """
        url = f"{API_URL}/catalog/discounts/{discount_id}"
        discount = discount_modification.model_dump(exclude_none=True)
        response = self._request(
            "PUT", url, expected_status=httpx.codes.OK, json=discount
        )
        return TactillResponse.model_validate(response)

    def get_option_lists(
        self,
        limit: int = 100,
        skip: int = 0,
        filter: str | None = None,
        order: str | None = None,
    ) -> list[OptionList]:
        """
        Get a list of OptionList based on the given filters.

        :param limit: Limit the number of returned records.
        :param skip: Define an offset in the returned records.
        :param filter: Allow filtering the results based on query language.
        :param order: Allow ordering by field (example "field1=ASC&field2=DESC").

        :return: A list of retrieved OptionLists.
        """
        url = f"{API_URL}/catalog/option_lists"
        params = {"node_id": self.node_id}
        response = self._get(url, params, limit, skip, filter, order)
        return [OptionList.model_validate(entity) for entity in response]

    def create_option_list(
        self, option_list_creation: OptionListCreation
    ) -> OptionList:
        """
        Create a new OptionList.

        :param option_list_creation: The OptionList creation data.

        :return: The created OptionList.
        """
        url = f"{API_URL}/catalog/option_lists"
        option_list = option_list_creation.model_dump(exclude_none=True)
        option_list["node_id"] = self.node_id

        response = self._request(
            "POST", url, expected_status=httpx.codes.CREATED, json=option_list
        )

        return OptionList.model_validate(response)

    def delete_option_list(self, option_list_id: TactillUUID) -> TactillResponse:
        """
        Delete an OptionList.

        :param option_list_id: The ID of the OptionList to be deleted.

        :return: A `TactillResponse` object representing the response from the API.
        """
        url = f"{API_URL}/catalog/option_lists/{option_list_id}"
        return self._delete(url)

    def get_option_list(self, option_list_id: TactillUUID) -> OptionList:
        """
        Get an OptionList by its unique id.

        :param option_list_id: The unique id of the OptionList.

        :return: The OptionList object with the corresponding id.
        """
        url = f"{API_URL}/catalog/option_lists/{option_list_id}"
        response = self._request("GET", url, expected_status=httpx.codes.OK)
        return OptionList.model_validate(response)

    def update_option_list(
        self,
        option_list_id: TactillUUID,
        option_list_modification: OptionListModification,
    ) -> TactillResponse:
        """
        Modify a OptionList.

        :param option_list_id: The unique id of the OptionList.
        :param option_list_modification: The OptionList modification data.

        :return: A `TactillResponse` object representing the response from the API.
        """
        url = f"{API_URL}/catalog/option_lists/{option_list_id}"
        option_list = option_list_modification.model_dump(exclude_none=True)
        response = self._request(
            "PUT", url, expected_status=httpx.codes.OK, json=option_list
        )
        return TactillResponse.model_validate(response)

    def get_options(
        self,
        limit: int = 100,
        skip: int = 0,
        filter: str | None = None,
        order: str | None = None,
    ) -> list[Option]:
        """
        Get a list of Option based on the given filters.

        :param limit: Limit the number of returned records.
        :param skip: Define an offset in the returned records.
        :param filter: Allow filtering the results based on query language.
        :param order: Allow ordering by field (example "field1=ASC&field2=DESC").

        :return: A list of retrieved Options.
        """
        url = f"{API_URL}/catalog/options"
        param = {"node_id": self.node_id}
        response = self._get(url, param, limit, skip, filter, order)
        return [Option.model_validate(entity) for entity in response]

    def create_option(self, option_creation: OptionCreation) -> Option:
        """
        Create a new Option.

        :param option_creation: The Option creation data.

        :return: The created Option.
        """
        url = f"{API_URL}/catalog/options"
        option = option_creation.model_dump(exclude_none=True)
        option["node_id"] = self.node_id

        response = self._request(
            "POST", url, expected_status=httpx.codes.CREATED, json=option
        )

        return Option.model_validate(response)

    def delete_option(self, option_id: TactillUUID) -> TactillResponse:
        """
        Delete an Option.

        :param option_id: The unique id of the Option to be deleted.

        :return: A `TactillResponse` object representing the response from the API.
        """
        url = f"{API_URL}/catalog/options/{option_id}"
        return self._delete(url)

    def get_option(self, option_id: TactillUUID) -> Option:
        """
        Get an Option by its unique id.

        :param option_id: The unique id of the Option.

        :return: The Option object with the corresponding ID.
        """
        url = f"{API_URL}/catalog/options/{option_id}"
        response = self._request("GET", url, expected_status=httpx.codes.OK)
        return Option.model_validate(response)

    def update_option(
        self,
        option_id: TactillUUID,
        option_modification: OptionModification,
    ) -> TactillResponse:
        """
        Modify an Option.

        :param option_id: The unique id of the Option.
        :param option_modification: The Option modification data.

        :return: A `TactillResponse` object representing the response from the API.
        """
        url = f"{API_URL}/catalog/options/{option_id}"
        option = option_modification.model_dump(exclude_none=True)
        response = self._request(
            "PUT", url, expected_status=httpx.codes.OK, json=option
        )
        return TactillResponse.model_validate(response)

    def get_packs(
        self,
        limit: int = 100,
        skip: int = 0,
        filter: str | None = None,
        order: str | None = None,
    ) -> list[Pack]:
        """
        Get a list of Pack based on the given filters.

        :param limit: Limit the number of returned records.
        :param skip: Define an offset in the returned records.
        :param filter: Allow filtering the results based on query language.
        :param order: Allow ordering by field (example "field1=ASC&field2=DESC").

        :return: A list of retrieved Packs.
        """
        url = f"{API_URL}/catalog/packs"
        param = {"node_id": self.node_id}
        response = self._get(url, param, limit, skip, filter, order)
        return [Pack.model_validate(entity) for entity in response]

    def create_pack(self, pack_creation: PackCreation) -> Pack:
        """
        Create a new Pack.

        :param pack_creation: The Pack creation data.

        :return: The created Pack.
        """
        url = f"{API_URL}/catalog/packs"
        pack = pack_creation.model_dump(exclude_none=True)
        pack["node_id"] = self.node_id

        response = self._request(
            "POST", url, expected_status=httpx.codes.CREATED, json=pack
        )

        return Pack.model_validate(response)

    def delete_pack(self, pack_id: TactillUUID) -> TactillResponse:
        """
        Delete a Pack.

        :param pack_id: The unique id of the Pack to be deleted.

        :return: A `TactillResponse` object representing the response from the API.
        """
        url = f"{API_URL}/catalog/packs/{pack_id}"
        return self._delete(url)

    def get_pack(self, pack_id: TactillUUID) -> Pack:
        """
        Get a Pack by its unique id.

        :param pack_id: The unique id of the Option.

        :return: The Pack object with the corresponding ID.
        """
        url = f"{API_URL}/catalog/packs/{pack_id}"
        response = self._request("GET", url, expected_status=httpx.codes.OK)
        return Pack.model_validate(response)

    def update_pack(
        self,
        pack_id: TactillUUID,
        pack_modification: PackModification,
    ) -> TactillResponse:
        """
        Modify a Pack.

        :param pack_id: The unique id of the Option.
        :param pack_modification: The Option modification data.

        :return: A `TactillResponse` object representing the response from the API.
        """
        url = f"{API_URL}/catalog/packs/{pack_id}"
        pack = pack_modification.model_dump(exclude_none=True)
        response = self._request("PUT", url, expected_status=httpx.codes.OK, json=pack)
        return TactillResponse.model_validate(response)

    def get_taxes(
        self,
        limit: int = 100,
        skip: int = 0,
        filter: str | None = None,
        order: str | None = None,
    ) -> list[Tax]:
        """
        Get a list of Tax based on the given filters.

        :param limit: Limit the number of returned records.
        :param skip: Define an offset in the returned records.
        :param filter: Allow filtering the results based on query language.
        :param order: Allow ordering by field (example "field1=ASC&field2=DESC").

        :return: A list of retrieved Taxes.
        """
        url = f"{API_URL}/catalog/taxes"
        param = {"company_id": self.company_id}
        response = self._get(url, param, limit, skip, filter, order)
        return [Tax.model_validate(entity) for entity in response]

    def create_tax(self, tax_creation: TaxCreation) -> Tax:
        """
        Create a new Tax.

        :param tax_creation: The Tax creation data.

        :return: The created Tax.
        """
        url = f"{API_URL}/catalog/taxes"
        tax = tax_creation.model_dump(exclude_none=True)
        tax["company_id"] = self.company_id

        response = self._request(
            "POST", url, expected_status=httpx.codes.CREATED, json=tax
        )

        return Tax.model_validate(response)

    def delete_tax(self, tax_id: TactillUUID) -> TactillResponse:
        """
        Delete a Tax.

        :param tax_id: The unique id of the Tax to be deleted.

        :return: A `TactillResponse` object representing the response from the API.
        """
        url = f"{API_URL}/catalog/taxes/{tax_id}"
        return self._delete(url)

    def get_tax(self, tax_id: TactillUUID) -> Tax:
        """
        Get a Tax by its unique id.

        :param tax_id: The unique id of the Tax.

        :return: The Tax object with the corresponding ID.
        """
        url = f"{API_URL}/catalog/taxes/{tax_id}"
        response = self._request("GET", url, expected_status=httpx.codes.OK)
        return Tax.model_validate(response)

    def update_tax(
        self,
        tax_id: TactillUUID,
        tax_modification: TaxModification,
    ) -> TactillResponse:
        """
        Modify a Tax.

        :param tax_id: The unique id of the Tax.
        :param tax_modification: The Tax modification data.

        :return: A `TactillResponse` object representing the response from the API.
        """
        url = f"{API_URL}/catalog/taxes/{tax_id}"
        tax = tax_modification.model_dump(exclude_none=True)
        response = self._request("PUT", url, expected_status=httpx.codes.OK, json=tax)
        return TactillResponse.model_validate(response)

    def get_movements(
        self,
        limit: int = 100,
        skip: int = 0,
        filter: str | None = None,
        order: str | None = None,
    ) -> list[Movement]:
        """
        Get a list of Movement based on the given filters.

        :param limit: Limit the number of returned records.
        :param skip: Define an offset in the returned records.
        :param filter: Allow filtering the results based on query language.
        :param order: Allow ordering by field (example "field1=ASC&field2=DESC").

        :return: A list of retrieved Movements.
        """
        url = f"{API_URL}/stock/movements"
        param = {"shop_id": self.shop_id}
        response = self._get(url, param, limit, skip, filter, order)
        return [Movement.model_validate(entity) for entity in response]

    def create_movement(self, movement_creation: MovementCreation) -> Movement:
        """
        Create a new Movement.

        :param movement_creation: The Movement creation data.

        :return: The created Movement.
        """
        url = f"{API_URL}/stock/movements"
        pack = movement_creation.model_dump(exclude_none=True)
        pack["shop_id"] = self.shop_id

        response = self._request(
            "POST", url, expected_status=httpx.codes.CREATED, json=pack
        )

        return Movement.model_validate(response)
