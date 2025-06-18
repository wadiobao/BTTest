import pytest
import pytest_asyncio
from httpx import AsyncClient

# --- Test Cases ---
@pytest.mark.asyncio
async def test_them_lop_hoc_thanh_cong(async_client: AsyncClient):
    lop_hoc_data = {
        "id": "TEST002",  # Use unique ID
        "ten_lop_hoc": "Test Lop 2",
        "si_so": 25
    }
    response = await async_client.post("/lophoc/lop/them/", json=lop_hoc_data)
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == 200
    result = data["result"]
    assert result["ten_lop_hoc"] == lop_hoc_data["ten_lop_hoc"]
    assert result["id"] == lop_hoc_data["id"]

@pytest.mark.asyncio
async def test_them_lop_hoc_khong_thanh_cong(async_client: AsyncClient):
    lop_hoc_data = {
        "id": "TEST002",  # Use unique ID
        "ten_lop_hoc": "Test Lop 2",
        "si_so": 25
    }
    response = await async_client.post("/lophoc/lop/them/", json=lop_hoc_data)
    assert response.status_code == 417
    data = response.json()
    assert data["code"] == 422
    result = data["result"]
    assert isinstance(result,str)
    

@pytest.mark.asyncio
async def test_hien_ds_lop_hoc_sau_khi_them(async_client: AsyncClient):
    response = await async_client.get("/lophoc/lop/hienthi/tatca")
    assert response.status_code == 200
    data = response.json()
    assert len(data["result"]) >= 1

@pytest.mark.asyncio
async def test_sua_lop_hoc(async_client: AsyncClient):
    update_data = {
        "id": "TEST001",
        "ten_lop_hoc": "Updated Lop",
        "si_so": 35
    }
    response = await async_client.patch("/lophoc/lop/sua/TEST001", json=update_data)
    assert response.status_code == 200
    data = response.json()
    result = data["result"]
    assert result["ten_lop_hoc"] == "Updated Lop"
    assert result["id"] == "TEST001"

@pytest.mark.asyncio
async def test_xoa_lop_hoc(async_client: AsyncClient):
    # First create a new lop hoc to delete
    lop_hoc_data = {
        "id": "DELETE",
        "ten_lop_hoc": "Lop De Xoa",
        "si_so": 20
    }
    create_response = await async_client.post("/lophoc/lop/them/", json=lop_hoc_data)
    assert create_response.status_code == 200
    # Now delete it
    response = await async_client.delete("/lophoc/lophoc/xoa/?id=DELETE")
    assert response.status_code == 200
    assert response.json()["code"] == 200

@pytest.mark.asyncio
async def test_hien_lop_hoc_khong_ton_tai(async_client: AsyncClient):
    response = await async_client.get("/lop-hoc/hien/NONEXISTENT")
    assert response.status_code == 404 
