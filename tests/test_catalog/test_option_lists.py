import httpx
import pytest

from tactill import QueryParams, TactillClient, TactillError
from tactill.entities.catalog.option import (
    OptionList,
    OptionListCreation,
    OptionListModification,
)
from tactill.filters import FilterEntity


@pytest.mark.vcr()
def test_get_option_lists(client: TactillClient) -> None:
    limit = 1
    query = QueryParams(limit=limit)
    option_lists = client.get_option_lists(query=query)

    assert len(option_lists) == limit


@pytest.mark.vcr()
def test_get_option_lists_with_skip(client: TactillClient) -> None:
    option_lists = client.get_option_lists()
    query = QueryParams(skip=1)
    option_lists_skip = client.get_option_lists(query=query)

    assert option_lists_skip[0] == option_lists[1]


@pytest.mark.vcr()
def test_get_option_lists_with_filter(client: TactillClient) -> None:
    option_list_name = "Test"
    query = QueryParams(filters=[FilterEntity(field="name", value=option_list_name)])
    option_lists = client.get_option_lists(query=query)

    option_list = option_lists[0]
    assert option_list.name == option_list_name


@pytest.mark.vcr()
def test_get_option_lists_with_order(client: TactillClient) -> None:
    query = QueryParams(order="name=ASC")
    option_lists = client.get_option_lists(query=query)

    names = [option_list.name for option_list in option_lists if option_list.name]
    sorted_names = sorted(names)
    assert names == sorted_names


@pytest.mark.vcr()
def test_create_option_list_bad_request(client: TactillClient) -> None:
    option_list_creation = OptionListCreation(
        options=["64e3230e2626360008a8ab07"],
        name="",
        multiple=False,
        mandatory=True,
    )
    with pytest.raises(TactillError) as excinfo:
        client.create_option_list(option_list_creation=option_list_creation)

    error = excinfo.value.error
    assert error.status_code == httpx.codes.BAD_REQUEST
    assert error.error == "Bad Request"
    assert error.message == "Invalid request payload input"


@pytest.mark.vcr()
def test_get_option_list(client: TactillClient, option_list: OptionList) -> None:
    created_option_list = client.get_option_list(option_list_id=option_list.id)

    assert created_option_list.id == option_list.id


@pytest.mark.vcr()
def test_get_option_list_not_found(client: TactillClient) -> None:
    option_list_id = "14e3250f2749240009abe5c1"

    with pytest.raises(TactillError) as excinfo:
        client.get_option_list(option_list_id=option_list_id)

    error = excinfo.value.error
    assert error.status_code == httpx.codes.NOT_FOUND
    assert error.error == "Not Found"
    assert error.message == '"option_list_id" specified in "params" could not be found'


@pytest.mark.vcr()
def test_get_option_list_bad_request(client: TactillClient) -> None:
    option_list_id = "1"

    with pytest.raises(TactillError) as excinfo:
        client.get_option_list(option_list_id=option_list_id)

    error = excinfo.value.error
    assert error.status_code == httpx.codes.BAD_REQUEST
    assert error.error == "Bad Request"


@pytest.mark.vcr()
def test_update_option_list_bad_request(
    client: TactillClient, option_list: OptionList
) -> None:
    option_list_modification = OptionListModification(
        options=["64e3230e2626360008a8ab07"], name=""
    )

    with pytest.raises(TactillError) as excinfo:
        client.update_option_list(
            option_list_id=option_list.id,
            option_list_modification=option_list_modification,
        )

    error = excinfo.value.error
    assert error.status_code == httpx.codes.BAD_REQUEST
    assert error.error == "Bad Request"
