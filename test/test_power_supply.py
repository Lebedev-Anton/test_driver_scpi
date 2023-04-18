import pytest

from src.services.power_supply import PowerSupply
from src.services.transport import TestTransport


@pytest.fixture
def power_supply(to_read: dict):
    transport = TestTransport(to_read)
    power_supply = PowerSupply(transport)
    power_supply.transport = transport
    return power_supply


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'answer, to_read, channel_params',
    [
        ({1: ':SOURce1:CURRent 1.5\n', 2: ':SOURce1:VOLTage 15\n', 3: ':OUTPut1:STATe ON\n'}, {}, [1, 1.5, 15]),
        ({1: ':SOURce2:CURRent 5\n', 2: ':SOURce2:VOLTage 25\n', 3: ':OUTPut2:STATe ON\n'}, {}, [2, 5, 25]),
        ({1: ':SOURce3:CURRent 6.2\n', 2: ':SOURce3:VOLTage 21\n', 3: ':OUTPut3:STATe ON\n'}, {}, [3, 6.2, 21]),
        ({1: ':SOURce4:CURRent 3\n', 2: ':SOURce4:VOLTage 21\n', 3: ':OUTPut4:STATe ON\n'}, {}, [4, 3, 21]),
    ],
)
async def test_turn_on_channel(power_supply, answer: dict, to_read: dict, channel_params: list):
    # act
    await power_supply.turn_on_channel(*channel_params)

    # assert
    assert power_supply.transport.writer == answer


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'channel_params, to_read',
    [
        ([5, 1.5, 15], {}),
        ([4, 15, 15], {}),
        ([4, 5, 150], {}),
    ],
)
async def test_turn_on_channel_with_bad_params(power_supply, channel_params: dict, to_read: dict):
    # act
    with pytest.raises(AssertionError):
        await power_supply.turn_on_channel(*channel_params)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'answer, to_read, channel',
    [
        ({1: ':OUTPut1:STATe OFF\n'}, {}, 1),
        ({1: ':OUTPut2:STATe OFF\n'}, {}, 2),
        ({1: ':OUTPut3:STATe OFF\n'}, {}, 3),
        ({1: ':OUTPut4:STATe OFF\n'}, {}, 4),
    ],
)
async def test_turn_off_channel(power_supply, answer: dict, to_read: dict, channel: int):
    # act
    await power_supply.turn_off_channel(channel)

    # assert
    assert power_supply.transport.writer == answer


@pytest.mark.asyncio
@pytest.mark.parametrize('to_read, channel', [({}, 5), ({}, -2)])
async def test_turn_off_channel_with_bad_params(power_supply, to_read: dict, channel: int):
    # act
    with pytest.raises(AssertionError):
        await power_supply.turn_off_channel(channel)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'answer, to_read, channel',
    [
        ({1: ':MEASure1:CURRent?\n', 2: ':MEASure1:VOLTage?\n', 3: ':MEASure1:POWEr?\n'}, {1: 6, 2: 15, 3: 20}, 1),
        ({1: ':MEASure2:CURRent?\n', 2: ':MEASure2:VOLTage?\n', 3: ':MEASure2:POWEr?\n'}, {1: 7, 2: 12, 3: 6}, 2),
        ({1: ':MEASure3:CURRent?\n', 2: ':MEASure3:VOLTage?\n', 3: ':MEASure3:POWEr?\n'}, {1: 0, 2: 4, 3: 9}, 3),
        ({1: ':MEASure4:CURRent?\n', 2: ':MEASure4:VOLTage?\n', 3: ':MEASure4:POWEr?\n'}, {1: 3, 2: 1, 3: 2}, 4),
    ],
)
async def test_get_channel_state(power_supply, answer: dict, to_read: dict, channel: int):
    # act
    current, voltage, power = await power_supply.get_channel_state(channel)

    # assert
    assert current == to_read.get(1)
    assert voltage == to_read.get(2)
    assert power == to_read.get(3)

    assert power_supply.transport.writer == answer


@pytest.mark.asyncio
@pytest.mark.parametrize('to_read, channel', [({}, 5), ({}, -2)])
async def test_get_channel_state_with_bad_params(power_supply, to_read: dict, channel: int):
    # act
    with pytest.raises(AssertionError):
        await power_supply.get_channel_state(channel)
