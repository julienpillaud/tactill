import httpx
import pytest

from tactill.entities.option import OptionListCreation
from tactill.tactill import ResponseError, TactillClient


def test_get_option_lists(client: TactillClient) -> None:
    limit = 1
    option_lists = client.get_option_lists(limit=limit)

    assert len(option_lists) == limit


def test_get_option_lists_with_skip(client: TactillClient) -> None:
    option_lists = client.get_option_lists()
    option_lists_skip = client.get_option_lists(skip=1)

    assert option_lists_skip[0] == option_lists[1]


def test_get_option_lists_with_filter(client: TactillClient) -> None:
    option_list_name = "Test"
    option_lists = client.get_option_lists(filter=f"name={option_list_name}")

    option_list = option_lists[0]
    assert option_list.name == option_list_name


def test_get_option_lists_with_order(client: TactillClient) -> None:
    option_lists = client.get_option_lists(order="name=ASC")

    names = [option_list.name for option_list in option_lists if option_list.name]
    sorted_names = sorted(names)
    assert names == sorted_names


def test_get_option_lists_bad_request(client: TactillClient) -> None:
    with pytest.raises(ResponseError) as excinfo:
        client.get_option_lists(filter="bad")

    error = excinfo.value.error
    assert error.status_code == httpx.codes.BAD_REQUEST
    assert error.error == "Bad Request"


def test_create_option_list(client: TactillClient) -> None:
    option_list_creation = OptionListCreation(
        options=["64e3230e2626360008a8ab07"],
        name="Test",
        multiple=False,
        mandatory=True,
    )

    option_list = client.create_option_list(option_list_creation=option_list_creation)

    assert option_list.options[0] == option_list_creation.options[0]
    assert option_list.name == option_list_creation.name
    assert option_list.multiple == option_list_creation.multiple
    assert option_list.mandatory == option_list_creation.mandatory

    client.delete_option_list(option_list_id=option_list.id)


def test_create_option_list_bad_request(client: TactillClient) -> None:
    option_list_creation = OptionListCreation(
        options=["64e3230e2626360008a8ab07"],
        name="",
        multiple=False,
        mandatory=True,
    )
    with pytest.raises(ResponseError) as excinfo:
        client.create_option_list(option_list_creation=option_list_creation)

    error = excinfo.value.error
    assert error.status_code == httpx.codes.BAD_REQUEST
    assert error.error == "Bad Request"
    assert (
        error.message
        == 'child "name" fails because ["name" is not allowed to be empty]'
    )


def test_get_option_list(client: TactillClient) -> None:
    option_list_id = "64e3250f2749240009abe5c1"
    option_list = client.get_option_list(option_list_id=option_list_id)

    assert option_list.id == option_list_id


def test_get_option_list_not_found(client: TactillClient) -> None:
    option_list_id = "14e3250f2749240009abe5c1"

    with pytest.raises(ResponseError) as excinfo:
        client.get_option_list(option_list_id=option_list_id)

    error = excinfo.value.error
    assert error.status_code == httpx.codes.NOT_FOUND
    assert error.error == "Not Found"
    assert error.message == '"option_list_id" specified in "params" could not be found'


def test_get_option_list_bad_request(client: TactillClient) -> None:
    option_list_id = "1"

    with pytest.raises(ResponseError) as excinfo:
        client.get_option_list(option_list_id=option_list_id)

    error = excinfo.value.error
    assert error.status_code == httpx.codes.BAD_REQUEST
    assert error.error == "Bad Request"
