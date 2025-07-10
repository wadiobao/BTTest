import pytest
import pytest_asyncio
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_read_main(async_client: AsyncClient):
    response = await async_client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}

@pytest.mark.asyncio
async def test_all_sinhvien(async_client: AsyncClient):
    response = await async_client.get("/sinhvien/hienthi/tatca")
    assert response.status_code == 200
    data = response.json()
    assert "code" in data
    assert "result" in data
    assert isinstance(data["result"], list)

@pytest.mark.asyncio
async def test_all_sinhvien_with_name(async_client: AsyncClient):
    response = await async_client.get("/sinhvien/hienthi/ten", params={"ten": "Bao"})
    assert response.status_code == 200
    data = response.json()
    assert "result" in data

@pytest.mark.asyncio
async def test_all_sinhvien_with_id(async_client: AsyncClient):
    response = await async_client.get("/sinhvien/hienthi/4")
    assert response.status_code == 200
    data = response.json()
    assert "code" in data
    assert "result" in data
    assert isinstance(data["result"], dict)

@pytest.mark.asyncio
async def test_chat_summary(async_client: AsyncClient):
    response = await async_client.post("/chat/summary/", data={"prompt": "Test message"})
    assert response.status_code == 200
    data = response.json()
    assert "code" in data
    assert "result" in data
    assert isinstance(data["result"], str)

