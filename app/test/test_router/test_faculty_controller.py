import pytest
import pytest_asyncio
from httpx import AsyncClient

# --- Test Cases ---
@pytest.mark.asyncio
async def test_faculty_list_when_db_not_empty(async_client: AsyncClient):
    response = await async_client.get("/faculty/all")
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == 200
    # Database has seeded data, so it's not empty
    assert len(data["result"]) >= 1

@pytest.mark.asyncio
async def test_faculty_create_success(async_client: AsyncClient):
    faculty_data = {
        "name": "Test Faculty",
        "id": "TEST"
    }
    response = await async_client.post("/faculty/create/", json=faculty_data)
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == 200
    result = data["result"]
    assert result["name"] == faculty_data["name"]
    assert result["id"] == faculty_data["id"]

@pytest.mark.asyncio
async def test_faculty_list_after_create(async_client: AsyncClient):
    response = await async_client.get("/faculty/all")
    assert response.status_code == 200
    data = response.json()
    assert len(data["result"]) >= 1

@pytest.mark.asyncio
async def test_faculty_get_by_id(async_client: AsyncClient):
    response = await async_client.get("/faculty/by-id/K01")
    assert response.status_code == 200
    data = response.json()
    assert data["result"]["name"] == "Công nghệ thông tin"

@pytest.mark.asyncio
async def test_faculty_update(async_client: AsyncClient):
    update_data = {
        "name": "Updated Faculty"
    }
    response = await async_client.patch("/faculty/update/K01", json=update_data)
    assert response.status_code == 200
    data = response.json()
    result = data["result"]
    assert result["name"] == "Updated Faculty"
    assert result["id"] == "K01"

@pytest.mark.asyncio
async def test_faculty_delete(async_client: AsyncClient):
    # First create a new faculty to delete
    faculty_data = {
        "name": "Faculty De Xoa",
        "id": "DELETE"
    }
    create_response = await async_client.post("/faculty/create/", json=faculty_data)
    assert create_response.status_code == 200
    # Now delete it
    response = await async_client.delete("/faculty/delete/?id=DELETE")
    assert response.status_code == 200
    assert response.json()["code"] == 200 
