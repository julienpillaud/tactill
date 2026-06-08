import pytest

from tactill import AsyncTactillClient
from tests.data import TAX_RATES


@pytest.mark.skip_on_ci
@pytest.mark.asyncio
async def test_get_taxes(aclient: AsyncTactillClient) -> None:
    results = await aclient.taxes.get_all()

    assert len(results) == len(TAX_RATES)
    for result in results:
        assert result.deprecated is False
        assert result.rate in TAX_RATES


@pytest.mark.skip_on_ci
@pytest.mark.asyncio
async def test_get_tax(aclient: AsyncTactillClient) -> None:
    results = await aclient.taxes.get_all()
    tax = results[0]

    response = await aclient.taxes.get(tax_id=tax.id)
    assert response.id == tax.id
    assert response.deprecated == tax.deprecated
    assert response.name == tax.name
    assert response.rate == tax.rate
