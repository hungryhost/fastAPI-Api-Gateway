import pytest
from httpx import AsyncClient

from app.main import app
from app.settings import settings


@pytest.mark.asyncio
async def test_root():

    async with AsyncClient(app=app, base_url=settings.app_url) as ac:
        response = await ac.get("/me")
    assert response.status_code == 200
    assert response.json() == {"message": "Tomato"}