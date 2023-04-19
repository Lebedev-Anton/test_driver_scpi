from http import HTTPStatus

import pytest

from src.api.v1.schemes import ChannelSates


@pytest.mark.parametrize('data', [{'channel': 1, 'current': 1, 'voltage': 10}])
def test_power_on(client, data: dict):
    # arrange
    url = 'api/v1/power_supply/power/on'

    # act
    response = client.post(url, json=data)
    body = response.json()

    # assert
    assert response.status_code == HTTPStatus.OK
    assert body == {
        'channel': 1,
        'state': 'on',
    }


@pytest.mark.parametrize(
    'data', [
        {'channel': 5, 'current': 1, 'voltage': 10},
        {'channel': 1, 'current': 8, 'voltage': 10},
        {'channel': 1, 'current': 4, 'voltage': 40},
    ],
)
def test_power_on_with_bad_params(client, data: dict):
    # arrange
    url = 'api/v1/power_supply/power/on'

    # act
    response = client.post(url, json=data)

    # assert
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


@pytest.mark.parametrize('data', [{'channel': 1}, {'channel': 2}, {'channel': 3}, {'channel': 4}])
def test_power_off(client, data: dict):
    # arrange
    url = 'api/v1/power_supply/power/off'

    # act
    response = client.post(url, json=data)
    body = response.json()

    # assert
    data['state'] = 'off'
    assert response.status_code == HTTPStatus.OK
    assert body == data


@pytest.mark.parametrize('data', [{'channel': -1}, {'channel': 0}, {'channel': 5}])
def test_power_off_with_bad_params(client, data: dict):
    # arrange
    url = 'api/v1/power_supply/power/off'

    # act
    response = client.post(url, json=data)

    # assert
    assert response.status_code == HTTPStatus.BAD_REQUEST


def test_state(client):
    # arrange
    url = 'api/v1/power_supply/state'

    # act
    response = client.get(url)
    body = response.json()

    # assert
    assert response.status_code == HTTPStatus.OK
    assert isinstance(ChannelSates(**body), ChannelSates)
