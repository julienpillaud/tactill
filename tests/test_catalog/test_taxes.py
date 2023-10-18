import httpx
import pytest

from tactill import ResponseError, TactillClient
from tactill.entities.catalog.tax import Tax, TaxCreation, TaxModification


def test_get_taxes(client: TactillClient) -> None:
    limit = 4
    taxes = client.get_taxes(limit=limit)

    assert len(taxes) == limit


def test_get_taxes_with_skip(client: TactillClient) -> None:
    taxes = client.get_taxes()
    taxes_skip = client.get_taxes(skip=1)

    assert taxes_skip[0] == taxes[1]


def test_get_taxes_with_filter(client: TactillClient) -> None:
    tax_name = "TVA 20"
    taxes = client.get_taxes(filter=f"name={tax_name}")

    tax = taxes[0]
    assert tax.name == tax_name


def test_get_taxes_with_order(client: TactillClient) -> None:
    taxes = client.get_taxes(order="name=ASC")

    names = [tax.name for tax in taxes if tax.name]
    sorted_names = sorted(names)
    assert names == sorted_names


def test_get_taxes_bad_request(client: TactillClient) -> None:
    with pytest.raises(ResponseError) as excinfo:
        client.get_taxes(filter="bad")

    error = excinfo.value.error
    assert error.status_code == httpx.codes.BAD_REQUEST
    assert error.error == "Bad Request"


def test_create_tax(client: TactillClient) -> None:
    tax_creation = TaxCreation(
        test=False,
        is_default=False,
        name="Test",
        in_price=True,
        rate=20,
    )
    tax = client.create_tax(tax_creation=tax_creation)

    assert tax.test == tax_creation.test
    assert tax.is_default == tax_creation.is_default
    assert tax.name == tax_creation.name
    assert tax.in_price == tax_creation.in_price
    assert tax.rate == tax_creation.rate

    client.delete_tax(tax.id)


def test_create_tax_bad_request(client: TactillClient) -> None:
    tax_creation = TaxCreation(
        is_default=False,
        name="",
        in_price=True,
        rate=20,
    )
    with pytest.raises(ResponseError) as excinfo:
        client.create_tax(tax_creation=tax_creation)

    error = excinfo.value.error
    assert error.status_code == httpx.codes.BAD_REQUEST
    assert error.error == "Bad Request"
    assert (
        error.message
        == 'child "name" fails because ["name" is not allowed to be empty]'
    )


def test_get_taxe(client: TactillClient) -> None:
    tax_id = "5d70d4e5be8f9f001195ccc3"
    tax = client.get_tax(tax_id=tax_id)

    assert tax.id == tax_id


def test_get_taxe_not_found(client: TactillClient) -> None:
    tax_id = "1d70d4e5be8f9f001195ccc3"

    with pytest.raises(ResponseError) as excinfo:
        client.get_tax(tax_id=tax_id)

    error = excinfo.value.error
    assert error.status_code == httpx.codes.NOT_FOUND
    assert error.error == "Not Found"
    assert error.message == '"tax_id" specified in "params" could not be found'


def test_get_taxe_bad_request(client: TactillClient) -> None:
    tax_id = "1"

    with pytest.raises(ResponseError) as excinfo:
        client.get_tax(tax_id=tax_id)

    error = excinfo.value.error
    assert error.status_code == httpx.codes.BAD_REQUEST
    assert error.error == "Bad Request"


def test_update_tax(client: TactillClient, tax: Tax) -> None:
    tax_modification = TaxModification(name="NEW NAME")

    response = client.update_tax(tax_id=tax.id, tax_modification=tax_modification)

    assert response.status_code == httpx.codes.OK
    assert response.message == "tax successfully updated"

    updated_tax = client.get_tax(tax_id=tax.id)

    assert updated_tax.version == tax.version
    assert updated_tax.deprecated == tax.deprecated
    assert updated_tax.created_at == tax.created_at
    assert updated_tax.updated_at != tax.updated_at
    assert updated_tax.original_id == tax.original_id

    assert updated_tax.company_id == tax.company_id

    assert updated_tax.test == tax.test
    assert updated_tax.is_default == tax.is_default
    assert updated_tax.name == tax_modification.name
    assert updated_tax.in_price == tax.in_price
    assert updated_tax.rate == tax.rate


def test_update_tax_bad_request(client: TactillClient, tax: Tax) -> None:
    tax_modification = TaxModification(name="")

    with pytest.raises(ResponseError) as excinfo:
        client.update_tax(
            tax_id=tax.id,
            tax_modification=tax_modification,
        )

    error = excinfo.value.error
    assert error.status_code == httpx.codes.BAD_REQUEST
    assert error.error == "Bad Request"
