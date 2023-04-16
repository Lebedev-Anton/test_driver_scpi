from http import HTTPStatus

from fastapi import APIRouter, Depends, Body
from fastapi.responses import JSONResponse
from src.services.power_supply import get_power_supply, PowerSupply
from src.api.v1.schemes import ChannelSettings, ChannelSates, ChannelParams, Error, PowerChannel

router: APIRouter = APIRouter()


@router.post('/power/on')
async def power_on(channel_setting: ChannelSettings, power_supply: PowerSupply = Depends(get_power_supply)):
    try:
        await power_supply.turn_on_channel(
            channel_setting.channel, channel_setting.current, channel_setting.voltage
        )
    except AssertionError:
        return JSONResponse(Error(message=f'Bad request').dict(), status_code=HTTPStatus.BAD_REQUEST)
    return JSONResponse(PowerChannel(channel=channel_setting.channel, state='on').dict(), status_code=HTTPStatus.OK)


@router.post('/power/off')
async def power_on(channel: int = Body(embed=True), power_supply: PowerSupply = Depends(get_power_supply)):
    try:
        await power_supply.turn_off_channel(channel)
    except AssertionError:
        return JSONResponse(Error(message=f'Bad request').dict(), status_code=HTTPStatus.BAD_REQUEST)
    return JSONResponse(PowerChannel(channel=channel, state='off').dict(), status_code=HTTPStatus.OK)


@router.get('/state')
async def get_channel_state(power_supply: PowerSupply = Depends(get_power_supply)):
    channel_1 = await power_supply.get_channel_state(1)
    channel_2 = await power_supply.get_channel_state(2)
    channel_3 = await power_supply.get_channel_state(3)
    channel_4 = await power_supply.get_channel_state(4)

    return ChannelSates(
        channel_1=ChannelParams(current=channel_1[0], voltage=channel_1[1], power=channel_1[2]),
        channel_2=ChannelParams(current=channel_2[0], voltage=channel_2[1], power=channel_2[2]),
        channel_3=ChannelParams(current=channel_3[0], voltage=channel_3[1], power=channel_3[2]),
        channel_4=ChannelParams(current=channel_4[0], voltage=channel_4[1], power=channel_4[2]),
    )
