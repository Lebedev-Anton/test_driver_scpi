import asyncio
import multiprocessing
import time

import aiohttp
import pytest
import pytest_asyncio


@pytest.fixture(autouse=True, scope='session')
def server_for_tests():
    from main import settings, uvicorn
    p = multiprocessing.Process(target=uvicorn.run, args=('main:app', ), kwargs={
        'port': 9000,
        'host': settings.APP_HOST,
        'reload': settings.DEBUG,
    })
    p.start()
    # Ожидаем запуск сервера
    # TODO заменить задержку
    time.sleep(2)
    yield
    p.terminate()


@pytest_asyncio.fixture(scope='session')
async def session():
    session = aiohttp.ClientSession()
    yield session
    await session.close()


@pytest_asyncio.fixture(scope='session')
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()
