from pydantic import BaseModel


class Error(BaseModel):
    message: str


class PowerChannel(BaseModel):
    channel: int
    state: str


class ChannelSettings(BaseModel):
    channel: int
    current: float
    voltage: float


class ChannelParams(BaseModel):
    current: float
    voltage: float
    power: float


class ChannelSates(BaseModel):
    channel_1: ChannelParams
    channel_2: ChannelParams
    channel_3: ChannelParams
    channel_4: ChannelParams
