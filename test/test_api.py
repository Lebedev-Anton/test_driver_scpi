from http import HTTPStatus

import pytest

from src.api.v1.schemes import ChannelSates


@pytest.mark.asyncio
async def test_power_on(session):
    url = 'http://127.0.0.1:8000/api/v1/power_supply/power/on'
    data = {
        'channel': 1,
        'current': 1,
        'voltage': 10,
    }
    async with session.post(url, json=data) as response:
        assert response.status == HTTPStatus.OK
        body = await response.json()
        assert body == {
            'channel': 1,
            'state': 'on',
        }

    data = {
        'channel': 5,
        'current': 1,
        'voltage': 10,
    }
    async with session.post(url, json=data) as response:
        assert response.status == HTTPStatus.UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_power_off(session):
    url = 'http://127.0.0.1:8000/api/v1/power_supply/power/off'
    data = {
        'channel': 1,
    }
    async with session.post(url, json=data) as response:
        assert response.status == HTTPStatus.OK
        body = await response.json()
        assert body == {
            'channel': 1,
            'state': 'off',
        }

    data = {
        'channel': 5,
    }
    async with session.post(url, json=data) as response:
        assert response.status == HTTPStatus.BAD_REQUEST


@pytest.mark.asyncio
async def test_state(session):
    url = 'http://127.0.0.1:8000/api/v1/power_supply/state'
    async with session.get(url) as response:
        assert response.status == HTTPStatus.OK
        body = await response.json()
        assert isinstance(ChannelSates(**body), ChannelSates)
