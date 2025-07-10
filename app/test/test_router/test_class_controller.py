import pytest
import pytest_asyncio
from httpx import AsyncClient

# --- Test Cases ---
@pytest.mark.asyncio
async def test_class_create_success(async_client: AsyncClient):
    class_data = {
        "id": "TEST002",  # Use unique ID
        "name": "Test Class 2",
        "capacity": 25
    }
    response = await async_client.post("/class/create/", json=class_data)
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == 200
    result = data["result"]
    assert result["name"] == class_data["name"]
    assert result["id"] == class_data["id"]

@pytest.mark.asyncio
async def test_class_create_fail(async_client: AsyncClient):
    class_data = {
        "id": "TEST002",  # Use unique ID
        "name": "Test Class 2",
        "capacity": 25
    }
    response = await async_client.post("/class/create/", json=class_data)
    assert response.status_code == 417
    data = response.json()
    assert data["code"] == 422
    result = data["result"]
    assert isinstance(result,str)
    

@pytest.mark.asyncio
async def test_class_list_after_create(async_client: AsyncClient):
    response = await async_client.get("/class/all")
    assert response.status_code == 200
    data = response.json()
    assert len(data["result"]) >= 1

@pytest.mark.asyncio
async def test_class_update(async_client: AsyncClient):
    update_data = {
        "id": "TEST001",
        "name": "Updated Class",
        "capacity": 35
    }
    response = await async_client.patch("/class/update/TEST001", json=update_data)
    assert response.status_code == 200
    data = response.json()
    result = data["result"]
    assert result["name"] == "Updated Class"
    assert result["id"] == "TEST001"

@pytest.mark.asyncio
async def test_class_delete(async_client: AsyncClient):
    # First create a new class to delete
    class_data = {
        "id": "DELETE",
        "name": "Class To Delete",
        "capacity": 20
    }
    create_response = await async_client.post("/class/create/", json=class_data)
    assert create_response.status_code == 200
    # Now delete it
    response = await async_client.delete("/class/delete/?id=DELETE")
    assert response.status_code == 200
    assert response.json()["code"] == 200

@pytest.mark.asyncio
async def test_class_get_nonexistent(async_client: AsyncClient):
    response = await async_client.get("/lop-hoc/hien/NONEXISTENT")
    assert response.status_code == 404 
