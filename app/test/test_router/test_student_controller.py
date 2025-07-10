import pytest
import pytest_asyncio
from httpx import AsyncClient

# --- Test Cases ---
@pytest.mark.asyncio
async def test_student_create_success(async_client: AsyncClient):
    student_data = {
        "name": "Student Moi",
        "gender": "Female",
        "birth_date": "2001-02-03",
        "phone": "0974745448",
        "email": "moi@example.com",
        "hometown": "Da Nang",
        "faculty_id": "K01"
    }
    response = await async_client.post("/student/create/", json=student_data)
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == 200
    created_id = data["result"]
    # Verify by GET
    get_response = await async_client.get(f"/student/by-id/{created_id}")
    assert get_response.status_code == 200
    result = get_response.json()["result"]
    assert result["name"] == student_data["name"]
    assert result["faculty"] == "Information Technology"

@pytest.mark.asyncio
async def test_student_create_fail(async_client: AsyncClient):
    student_data = {
        "name": "Student Moi",
        "gender": "N",
        "birth_date": "2001-02-03",
        "phone": "097",
        "email": "moi@example.com",
        "hometown": "Da Nang",
        "faculty_id": "K01"
    }
    response = await async_client.post("/student/create/", json=student_data)
    assert response.status_code == 417
    data = response.json()
    assert data["code"] == 422
    result = data["result"]
    assert isinstance(result,str)
    
@pytest.mark.asyncio
async def test_student_list_after_create(async_client: AsyncClient):
    response = await async_client.get("/student/all")
    assert response.status_code == 200
    data = response.json()
    assert len(data["result"]) >= 1

@pytest.mark.asyncio
async def test_student_get_by_id(async_client: AsyncClient):
    response = await async_client.get("/student/by-id/4")
    assert response.status_code == 200
    data = response.json()
    assert data["result"]["name"] == "Bao"

@pytest.mark.asyncio
async def test_student_get_by_name(async_client: AsyncClient):
    response = await async_client.get("/student/by-name", params={"name": "Bao"})
    assert response.status_code == 200
    data = response.json()
    assert len(data["result"]) >= 1
    assert data["result"][0]["name"] == "Bao"

@pytest.mark.asyncio
async def test_student_update(async_client: AsyncClient):
    # Need to provide all required fields for update
    update_data = {
        "name": "Ten Da Duoc Cap Nhat",
        "gender": "Nam",
        "birth_date": "2000-01-01",
        "phone": "0123456789",
        "email": "bao@example.com",
        "hometown": "Hanoi",
        "faculty_id": "K01"
    }
    response = await async_client.patch("/student/update/4", json=update_data)
    assert response.status_code == 200
    data = response.json()
    # data["result"] is a SinhVienResponse object, not an id
    result = data["result"]
    assert result["name"] == "Ten Da Duoc Cap Nhat"
    assert result["email"] == "bao@example.com"
    # Verify by GET using the id from the response
    updated_id = result["id"]
    get_response = await async_client.get(f"/student/by-id/{updated_id}")
    assert get_response.status_code == 200
    get_result = get_response.json()["result"]
    assert get_result["name"] == "Ten Da Duoc Cap Nhat"
    assert get_result["email"] == "bao@example.com"

@pytest.mark.asyncio
async def test_student_delete(async_client: AsyncClient):
    # First create a new sinh vien to delete
    student_data = {
        "name": "Sinh Vien De Xoa",
        "gender": "Nam",
        "birth_date": "2000-01-01",
        "phone": "0987654321",
        "email": "xoa@example.com",
        "hometown": "Ha Noi",
        "faculty_id": "K01"
    }
    create_response = await async_client.post("/student/create/", json=student_data)
    assert create_response.status_code == 200
    created_id = create_response.json()["result"]
    # Now delete it
    response = await async_client.delete(f"/student/delete/?id={created_id}")
    assert response.status_code == 200
    assert response.json()["code"] == 200
    # Verify it's deleted - expect exception or 404
    try:
        get_response = await async_client.get(f"/student/by-id/{created_id}")
        # If no exception, should be 404
        assert get_response.status_code == 404
    except Exception as e:
        # If exception occurs, should contain "does not exist"
        assert "does not exist" in str(e)
