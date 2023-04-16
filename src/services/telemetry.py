import asyncio
import logging
from logging import config

from logger import LOGGING
from src.services.power_supply import PowerSupply


class Telemetry:
    def __init__(self, power_supply: PowerSupply):
        self._power_supply = power_supply
        config.dictConfig(LOGGING)
        self.logger = logging.getLogger('power_supply_log')

    async def telemetry_run(self) -> None:
        while True:
            current, voltage, power = await self._power_supply.get_channel_state(1)
            self.log_telemetry(1, current, voltage, power)

            current, voltage, power = await self._power_supply.get_channel_state(2)
            self.log_telemetry(2, current, voltage, power)

            current, voltage, power = await self._power_supply.get_channel_state(3)
            self.log_telemetry(3, current, voltage, power)

            current, voltage, power = await self._power_supply.get_channel_state(4)
            self.log_telemetry(4, current, voltage, power)
            await asyncio.sleep(1)

    def log_telemetry(self, channel, current, voltage, power) -> None:
        self.logger.info(f'channel: {channel}, current: {current}, voltage: {voltage}, power: {power}')
