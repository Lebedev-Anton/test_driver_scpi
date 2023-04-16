import asyncio

import uvicorn as uvicorn
from fastapi import FastAPI

from settings import settings
from src.api.v1.endpoints import router
from src.services.power_supply import get_power_supply
from src.services.telemetry import Telemetry

app = FastAPI(
    title=settings.PROJECT_NAME,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    description='Информация о фильмах и рекомендациях пользователям',
    version='1.0.0',
)


@app.on_event('startup')
async def startup():
    telemetry = Telemetry(power_supply=get_power_supply())
    asyncio.create_task(telemetry.telemetry_run())


app.include_router(router, prefix='/api/v1/power_supply', tags=['power_supply'])

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host=settings.APP_HOST,
        port=settings.APP_PORT,
        reload=settings.DEBUG,
    )
