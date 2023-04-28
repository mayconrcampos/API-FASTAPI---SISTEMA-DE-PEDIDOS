import pytest_asyncio
from typing import AsyncIterator
from main import app
import httpx
import asyncio
from core.deps import get_session, get_session_test

app.dependency_overrides[get_session] = get_session_test

@pytest_asyncio.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def client(event_loop) -> AsyncIterator[httpx.AsyncClient]:
    async with httpx.AsyncClient(app=app, base_url="http://tests") as client:
        yield client


