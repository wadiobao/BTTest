import pytest
import pytest_asyncio
from httpx import AsyncClient

# --- Test Cases ---
@pytest.mark.asyncio
async def test_hien_ds_khoa_khi_db_rong(async_client: AsyncClient):
    response = await async_client.get("/khoa/hienthi/tatca")
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == 200
    # Database has seeded data, so it's not empty
    assert len(data["result"]) >= 1

@pytest.mark.asyncio
async def test_them_khoa_thanh_cong(async_client: AsyncClient):
    khoa_data = {
        "ten_khoa": "Test Khoa",
        "id": "TEST"
    }
    response = await async_client.post("/khoa/them/", json=khoa_data)
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == 200
    result = data["result"]
    assert result["ten_khoa"] == khoa_data["ten_khoa"]
    assert result["id"] == khoa_data["id"]

@pytest.mark.asyncio
async def test_hien_ds_khoa_sau_khi_them(async_client: AsyncClient):
    response = await async_client.get("/khoa/hienthi/tatca")
    assert response.status_code == 200
    data = response.json()
    assert len(data["result"]) >= 1

@pytest.mark.asyncio
async def test_hien_khoa_theo_id(async_client: AsyncClient):
    response = await async_client.get("/khoa/hienthi/K01")
    assert response.status_code == 200
    data = response.json()
    assert data["result"]["ten_khoa"] == "Công nghệ thông tin"

@pytest.mark.asyncio
async def test_sua_khoa(async_client: AsyncClient):
    update_data = {
        "ten_khoa": "Updated Khoa"
    }
    response = await async_client.patch("/khoa/sua/K01", json=update_data)
    assert response.status_code == 200
    data = response.json()
    result = data["result"]
    assert result["ten_khoa"] == "Updated Khoa"
    assert result["id"] == "K01"

@pytest.mark.asyncio
async def test_xoa_khoa(async_client: AsyncClient):
    # First create a new khoa to delete
    khoa_data = {
        "ten_khoa": "Khoa De Xoa",
        "id": "DELETE"
    }
    create_response = await async_client.post("/khoa/them/", json=khoa_data)
    assert create_response.status_code == 200
    # Now delete it
    response = await async_client.delete("/khoa/xoa/?id=DELETE")
    assert response.status_code == 200
    assert response.json()["code"] == 200 
