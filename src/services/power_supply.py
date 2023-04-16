from functools import lru_cache
from typing import NewType
from src.services.transport import SCPI, TestTransport


Power = NewType('Power', float)
Current = NewType('Current', float)
Voltage = NewType('Voltage', float)


class PowerSupply:
    _allowed_channels: list = [1, 2, 3, 4]

    _max_current = 6.2
    _min_current = 0

    _max_voltage = 35
    _min_voltage = 0

    def __init__(self, scpi: SCPI):
        self._scpi = scpi

    async def turn_on_channel(self, channel: int, current: float, voltage: float) -> None:
        assert channel in self._allowed_channels
        assert self._min_current <= current <= self._max_current
        assert self._min_voltage <= voltage <= self._max_voltage

        command = f':SOURce{channel}:CURRent {current}'
        await self._scpi.write(command)

        command = f':SOURce{channel}:VOLTage {voltage}'
        await self._scpi.write(command)

        command = f':OUTPut{channel}:STATe ON'
        await self._scpi.write(command)

    async def turn_off_channel(self, channel: int) -> None:
        assert channel in self._allowed_channels

        command = f':OUTPut{channel}:STATe OFF'
        await self._scpi.write(command)

    async def get_channel_state(self, channel: int) -> (Current, Voltage, Power):
        assert channel in self._allowed_channels
        command = f':MEASure{channel}:CURRent?'
        current = await self._scpi.query(command)

        command = f':MEASure{channel}:VOLTage?'
        voltage = await self._scpi.query(command)

        command = f':MEASure{channel}:POWEr?'
        power = await self._scpi.query(command)

        return current, voltage, power


@lru_cache()
def get_power_supply() -> PowerSupply:
    transport: SCPI = TestTransport(
        {
            1: 10,
            2: 15,
            3: 20,
        }
    )
    return PowerSupply(transport)
