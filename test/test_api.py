from http import HTTPStatus

import pytest

from src.api.v1.schemes import ChannelSates


@pytest.mark.asyncio
@pytest.mark.parametrize('data', [{'channel': 1, 'current': 1, 'voltage': 10}])
async def test_power_on(session, data: dict):
    # arrange
    url = 'http://127.0.0.1:9000/api/v1/power_supply/power/on'

    # act
    async with session.post(url, json=data) as response:
        body = await response.json()

    # assert
    assert response.status == HTTPStatus.OK
    assert body == {
        'channel': 1,
        'state': 'on',
    }


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'data', [
        {'channel': 5, 'current': 1, 'voltage': 10},
        {'channel': 1, 'current': 8, 'voltage': 10},
        {'channel': 1, 'current': 4, 'voltage': 40},
    ],
)
async def test_power_on_with_bad_params(session, data: dict):
    # arrange
    url = 'http://127.0.0.1:9000/api/v1/power_supply/power/on'

    # act
    async with session.post(url, json=data) as response:
        await response.json()

    # assert
    assert response.status == HTTPStatus.UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
@pytest.mark.parametrize('data', [{'channel': 1}, {'channel': 2}, {'channel': 3}, {'channel': 4}])
async def test_power_off(session, data: dict):
    # arrange
    url = 'http://127.0.0.1:9000/api/v1/power_supply/power/off'

    # act
    async with session.post(url, json=data) as response:
        body = await response.json()

    # assert
    data['state'] = 'off'
    assert response.status == HTTPStatus.OK
    assert body == data


@pytest.mark.asyncio
@pytest.mark.parametrize('data', [{'channel': -1}, {'channel': 0}, {'channel': 5}])
async def test_power_off_with_bad_params(session, data: dict):
    # arrange
    url = 'http://127.0.0.1:9000/api/v1/power_supply/power/off'

    # act
    async with session.post(url, json=data) as response:
        await response.json()

    # assert
    assert response.status == HTTPStatus.BAD_REQUEST


@pytest.mark.asyncio
async def test_state(session):
    # arrange
    url = 'http://127.0.0.1:9000/api/v1/power_supply/state'

    # act
    async with session.get(url) as response:
        body = await response.json()

    # assert
    assert response.status == HTTPStatus.OK
    assert isinstance(ChannelSates(**body), ChannelSates)
