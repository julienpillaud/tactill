import httpx
import pytest

from tactill.entities.option import Option, OptionCreation, OptionModification
from tactill.tactill import ResponseError, TactillClient


def test_get_options(client: TactillClient) -> None:
    limit = 1
    options = client.get_options(limit=limit)

    assert len(options) == limit


def test_get_options_with_skip(client: TactillClient) -> None:
    options = client.get_options()
    options_skip = client.get_options(skip=1)

    assert options_skip[0] == options[1]


def test_get_options_with_filter(client: TactillClient) -> None:
    option_name = "Test"
    options = client.get_options(filter=f"name={option_name}")

    option = options[0]
    assert option.name == option_name


def test_get_options_with_order(client: TactillClient) -> None:
    options = client.get_options(order="name=ASC")

    names = [option.name for option in options if option.name]
    sorted_names = sorted(names)
    assert names == sorted_names


def test_get_options_bad_request(client: TactillClient) -> None:
    with pytest.raises(ResponseError) as excinfo:
        client.get_options(filter="bad")

    error = excinfo.value.error
    assert error.status_code == httpx.codes.BAD_REQUEST
    assert error.error == "Bad Request"


def test_create_option(client: TactillClient) -> None:
    option_creation = OptionCreation(test=False, name="Test", price=1)

    option = client.create_option(option_creation=option_creation)

    assert option.test == option_creation.test
    assert option.name == option_creation.name
    assert option.price == option_creation.price

    client.delete_option(option_id=option.id)


def test_create_option_bad_request(client: TactillClient) -> None:
    option_creation = OptionCreation(test=False, name="", price=1)
    with pytest.raises(ResponseError) as excinfo:
        client.create_option(option_creation=option_creation)

    error = excinfo.value.error
    assert error.status_code == httpx.codes.BAD_REQUEST
    assert error.error == "Bad Request"
    assert (
        error.message
        == 'child "name" fails because ["name" is not allowed to be empty]'
    )


def test_get_option(client: TactillClient) -> None:
    option_id = "64e3230e2626360008a8ab07"
    option = client.get_option(option_id=option_id)

    assert option.id == option_id


def test_get_option_not_found(client: TactillClient) -> None:
    option_id = "14e3230e2626360008a8ab07"

    with pytest.raises(ResponseError) as excinfo:
        client.get_option(option_id=option_id)

    error = excinfo.value.error
    assert error.status_code == httpx.codes.NOT_FOUND
    assert error.error == "Not Found"
    assert error.message == '"option_id" specified in "params" could not be found'


def test_get_option_bad_request(client: TactillClient) -> None:
    option_id = "1"

    with pytest.raises(ResponseError) as excinfo:
        client.get_option(option_id=option_id)

    error = excinfo.value.error
    assert error.status_code == httpx.codes.BAD_REQUEST
    assert error.error == "Bad Request"


def test_update_option(client: TactillClient, option: Option) -> None:
    option_modification = OptionModification(name="NEW NAME")

    response = client.update_option(
        option_id=option.id, option_modification=option_modification
    )

    assert response.status_code == httpx.codes.OK
    assert response.message == "option successfully updated"

    updated_option = client.get_option(option_id=option.id)

    assert updated_option.version == option.version
    assert updated_option.deprecated == option.deprecated
    assert updated_option.created_at == option.created_at
    assert updated_option.updated_at != option.updated_at
    assert updated_option.original_id == option.original_id

    assert updated_option.node_id == option.node_id

    assert updated_option.test == option.test
    assert updated_option.name == option_modification.name
    assert updated_option.price == option.price


def test_update_option_bad_request(client: TactillClient, option: Option) -> None:
    option_modification = OptionModification(name="")

    with pytest.raises(ResponseError) as excinfo:
        client.update_option(
            option_id=option.id,
            option_modification=option_modification,
        )

    error = excinfo.value.error
    assert error.status_code == httpx.codes.BAD_REQUEST
    assert error.error == "Bad Request"
