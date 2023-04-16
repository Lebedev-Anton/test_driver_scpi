import pytest

from src.services.power_supply import PowerSupply
from src.services.transport import TestTransport


@pytest.mark.asyncio
async def test_turn_on_channel():
    answer = {
        1: ':SOURce1:CURRent 1.5\n',
        2: ':SOURce1:VOLTage 15\n',
        3: ':OUTPut1:STATe ON\n',

        4: ':SOURce2:CURRent 1.5\n',
        5: ':SOURce2:VOLTage 15\n',
        6: ':OUTPut2:STATe ON\n',

        7: ':SOURce3:CURRent 1.5\n',
        8: ':SOURce3:VOLTage 15\n',
        9: ':OUTPut3:STATe ON\n',

        10: ':SOURce4:CURRent 1.5\n',
        11: ':SOURce4:VOLTage 15\n',
        12: ':OUTPut4:STATe ON\n',
    }

    transport = TestTransport({})
    power_supply = PowerSupply(transport)
    await power_supply.turn_on_channel(1, 1.5, 15)
    await power_supply.turn_on_channel(2, 1.5, 15)
    await power_supply.turn_on_channel(3, 1.5, 15)
    await power_supply.turn_on_channel(4, 1.5, 15)

    assert transport.writer == answer

    with pytest.raises(AssertionError):
        await power_supply.turn_on_channel(5, 1.5, 15)

    with pytest.raises(AssertionError):
        await power_supply.turn_on_channel(4, 15, 15)

    with pytest.raises(AssertionError):
        await power_supply.turn_on_channel(4, 5, 150)


@pytest.mark.asyncio
async def test_turn_off_channel():
    answer = {
        1: ':OUTPut1:STATe OFF\n',
    }

    transport = TestTransport({})
    power_supply = PowerSupply(transport)
    await power_supply.turn_off_channel(1)

    assert transport.writer == answer

    with pytest.raises(AssertionError):
        await power_supply.turn_off_channel(5)


@pytest.mark.asyncio
async def test_get_channel_state():
    answer = {
        1: ':MEASure1:CURRent?\n',
        2: ':MEASure1:VOLTage?\n',
        3: ':MEASure1:POWEr?\n',

    }
    to_read = {
        1: 6,
        2: 15,
        3: 20,
    }

    transport = TestTransport(to_read)
    power_supply = PowerSupply(transport)
    current, voltage, power = await power_supply.get_channel_state(1)

    assert (current, voltage, power) == (6, 15, 20)

    assert transport.writer == answer

    with pytest.raises(AssertionError):
        await power_supply.turn_off_channel(5)
