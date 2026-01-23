import httpx
import pytest

from tactill import QueryParams, TactillClient, TactillError
from tactill.entities.catalog.option import Option, OptionCreation, OptionModification
from tactill.filters import FilterEntity


@pytest.mark.vcr()
def test_get_options(client: TactillClient) -> None:
    limit = 1
    query = QueryParams(limit=limit)
    options = client.get_options(query=query)

    assert len(options) == limit


@pytest.mark.vcr()
def test_get_options_with_skip(client: TactillClient) -> None:
    options = client.get_options()
    query = QueryParams(skip=1)
    options_skip = client.get_options(query=query)

    assert options_skip[0] == options[1]


@pytest.mark.vcr()
def test_get_options_with_filter(client: TactillClient) -> None:
    option_name = "Test"
    query = QueryParams(filters=[FilterEntity(field="name", value=option_name)])
    options = client.get_options(query=query)

    option = options[0]
    assert option.name == option_name


@pytest.mark.vcr()
def test_get_options_with_order(client: TactillClient) -> None:
    query = QueryParams(order="name=ASC")
    options = client.get_options(query=query)

    names = [option.name for option in options if option.name]
    sorted_names = sorted(names)
    assert names == sorted_names


@pytest.mark.vcr()
def test_create_option_bad_request(client: TactillClient) -> None:
    option_creation = OptionCreation(test=False, name="", price=1)
    with pytest.raises(TactillError) as excinfo:
        client.create_option(option_creation=option_creation)

    error = excinfo.value.error
    assert error.status_code == httpx.codes.BAD_REQUEST
    assert error.error == "Bad Request"
    assert error.message == "Invalid request payload input"


@pytest.mark.vcr()
def test_get_option(client: TactillClient, option: Option) -> None:
    created_option = client.get_option(option_id=option.id)

    assert created_option.id == option.id


@pytest.mark.vcr()
def test_get_option_not_found(client: TactillClient) -> None:
    option_id = "14e3230e2626360008a8ab07"

    with pytest.raises(TactillError) as excinfo:
        client.get_option(option_id=option_id)

    error = excinfo.value.error
    assert error.status_code == httpx.codes.NOT_FOUND
    assert error.error == "Not Found"
    assert error.message == '"option_id" specified in "params" could not be found'


@pytest.mark.vcr()
def test_get_option_bad_request(client: TactillClient) -> None:
    option_id = "1"

    with pytest.raises(TactillError) as excinfo:
        client.get_option(option_id=option_id)

    error = excinfo.value.error
    assert error.status_code == httpx.codes.BAD_REQUEST
    assert error.error == "Bad Request"


@pytest.mark.vcr()
def test_update_option_bad_request(client: TactillClient, option: Option) -> None:
    option_modification = OptionModification(name="")

    with pytest.raises(TactillError) as excinfo:
        client.update_option(
            option_id=option.id,
            option_modification=option_modification,
        )

    error = excinfo.value.error
    assert error.status_code == httpx.codes.BAD_REQUEST
    assert error.error == "Bad Request"
