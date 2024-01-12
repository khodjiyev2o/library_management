import pytest
from app.main import app
from httpx import AsyncClient
from app.db import engine
from app.models.models import Base


@pytest.fixture(scope='session')
async def client():
    async with (AsyncClient(app=app, base_url='http://localhost:8000', headers={'Content-Type': 'application/json'}) as
                client):
        yield client


@pytest.fixture(scope='session')
def anyio_backend():
    return 'asyncio'


@pytest.fixture(scope='module')
async def refresh_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture(scope='module')
async def clear_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
