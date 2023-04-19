import asyncio

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient

from main import app


@pytest.fixture(scope='session')
def client():
    return TestClient(app)


@pytest_asyncio.fixture(scope='session')
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()
