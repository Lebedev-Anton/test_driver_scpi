import datetime
from typing import Literal

from pydantic import BaseModel, confloat, conint


class Error(BaseModel):
    message: str


class PowerChannel(BaseModel):
    channel: conint(ge=1, le=4)
    state: Literal['on', 'off']


class ChannelSettings(BaseModel):
    channel: conint(ge=1, le=4)
    current: confloat(ge=0, le=6.2)
    voltage: confloat(ge=0, le=35)


class ChannelParams(BaseModel):
    meas_time: str = datetime.datetime.utcnow()
    current: confloat(ge=0, le=6.2)
    voltage: confloat(ge=0, le=35)
    power: float


class ChannelSates(BaseModel):
    channel_1: ChannelParams
    channel_2: ChannelParams
    channel_3: ChannelParams
    channel_4: ChannelParams
