import pytest

from myVaillant.api import MyVaillantAPI
from myVaillant.tests.utils import _mocked_api, _myVaillant_aioresponses


@pytest.fixture
def myVaillant_aioresponses():
    return _myVaillant_aioresponses()


@pytest.fixture
async def mocked_api() -> MyVaillantAPI:
    return await _mocked_api()
