import httpx
import pytest

from tactill import QueryParams, TactillClient, TactillError
from tactill.entities.catalog.tax import Tax, TaxCreation, TaxModification
from tactill.filters import FilterEntity


@pytest.mark.vcr()
def test_get_taxes(client: TactillClient) -> None:
    limit = 4
    query = QueryParams(limit=limit)
    taxes = client.get_taxes(query=query)

    assert len(taxes) == limit


@pytest.mark.vcr()
def test_get_taxes_with_skip(client: TactillClient) -> None:
    taxes = client.get_taxes()
    query = QueryParams(skip=1)
    taxes_skip = client.get_taxes(query=query)

    assert taxes_skip[0] == taxes[1]


@pytest.mark.vcr()
def test_get_taxes_with_filter(client: TactillClient) -> None:
    tax_name = "TVA 20"
    query = QueryParams(filters=[FilterEntity(field="name", value=tax_name)])
    taxes = client.get_taxes(query=query)

    tax = taxes[0]
    assert tax.name == tax_name


@pytest.mark.vcr()
def test_get_taxes_with_order(client: TactillClient) -> None:
    query = QueryParams(order="name=ASC")
    taxes = client.get_taxes(query=query)

    names = [tax.name for tax in taxes if tax.name]
    sorted_names = sorted(names)
    assert names == sorted_names


@pytest.mark.vcr()
def test_create_tax_bad_request(client: TactillClient) -> None:
    tax_creation = TaxCreation(
        is_default=False,
        name="",
        in_price=True,
        rate=20,
    )
    with pytest.raises(TactillError) as excinfo:
        client.create_tax(tax_creation=tax_creation)

    error = excinfo.value.error
    assert error.status_code == httpx.codes.BAD_REQUEST
    assert error.error == "Bad Request"
    assert error.message == "Invalid request payload input"


@pytest.mark.vcr()
def test_get_tax(client: TactillClient, tax: Tax) -> None:
    created_tax = client.get_tax(tax_id=tax.id)

    assert created_tax.id == tax.id


@pytest.mark.vcr()
def test_get_taxe_not_found(client: TactillClient) -> None:
    tax_id = "1d70d4e5be8f9f001195ccc3"

    with pytest.raises(TactillError) as excinfo:
        client.get_tax(tax_id=tax_id)

    error = excinfo.value.error
    assert error.status_code == httpx.codes.NOT_FOUND
    assert error.error == "Not Found"
    assert error.message == '"tax_id" specified in "params" could not be found'


@pytest.mark.vcr()
def test_get_taxe_bad_request(client: TactillClient) -> None:
    tax_id = "1"

    with pytest.raises(TactillError) as excinfo:
        client.get_tax(tax_id=tax_id)

    error = excinfo.value.error
    assert error.status_code == httpx.codes.BAD_REQUEST
    assert error.error == "Bad Request"


@pytest.mark.vcr()
def test_update_tax_bad_request(client: TactillClient, tax: Tax) -> None:
    tax_modification = TaxModification(name="")

    with pytest.raises(TactillError) as excinfo:
        client.update_tax(
            tax_id=tax.id,
            tax_modification=tax_modification,
        )

    error = excinfo.value.error
    assert error.status_code == httpx.codes.BAD_REQUEST
    assert error.error == "Bad Request"
