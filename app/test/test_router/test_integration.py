import pytest
import pytest_asyncio
from httpx import AsyncClient

"""
Integration Tests - Testing main functionality with unified database
This file tests the core functionality that we know works
"""

@pytest.mark.asyncio
async def test_main_endpoint(async_client: AsyncClient):
    """Test the main endpoint"""
    response = await async_client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}

@pytest.mark.asyncio
async def test_sinh_vien_list(async_client: AsyncClient):
    """Test getting all sinh vien"""
    response = await async_client.get("/sinhvien/hienthi/tatca")
    assert response.status_code == 200
    data = response.json()
    assert "code" in data
    assert "result" in data
    # Should have at least the seeded data
    assert len(data["result"]) >= 1

@pytest.mark.asyncio
async def test_sinh_vien_by_id(async_client: AsyncClient):
    """Test getting sinh vien by ID"""
    response = await async_client.get("/sinhvien/hienthi/4")
    assert response.status_code == 200
    data = response.json()
    assert data["result"]["ten_sinh_vien"] == "Bao"
    assert data["result"]["email"] == "bao@example.com"

@pytest.mark.asyncio
async def test_sinh_vien_by_name(async_client: AsyncClient):
    """Test getting sinh vien by name"""
    response = await async_client.get("/sinhvien/hienthi/ten?ten=Bao")
    assert response.status_code == 200
    data = response.json()
    assert len(data["result"]) >= 1
    assert data["result"][0]["ten_sinh_vien"] == "Bao"

@pytest.mark.asyncio
async def test_khoa_list(async_client: AsyncClient):
    """Test getting all khoa"""
    response = await async_client.get("/khoa/hienthi/tatca")
    assert response.status_code == 200
    data = response.json()
    assert "code" in data
    assert "result" in data
    # Should have at least the seeded data
    assert len(data["result"]) >= 1

@pytest.mark.asyncio
async def test_lop_hoc_list(async_client: AsyncClient):
    """Test getting all lop hoc"""
    response = await async_client.get("/lophoc/lop/hienthi/tatca")
    assert response.status_code == 200
    data = response.json()
    assert "code" in data
    assert "result" in data
    # Should have at least the seeded data
    assert len(data["result"]) >= 1

@pytest.mark.asyncio
async def test_chat_summary(async_client: AsyncClient):
    """Test chat summary endpoint"""
    response = await async_client.post("/chat/summary/", data={"prompt": "Test message"})
    assert response.status_code == 200
    data = response.json()
    assert "code" in data
    assert "result" in data
    assert isinstance(data["result"], str)

@pytest.mark.asyncio
async def test_database_consistency(async_client: AsyncClient):
    """Test that database is consistent across requests"""
    # First request
    response1 = await async_client.get("/sinhvien/hienthi/tatca")
    assert response1.status_code == 200
    data1 = response1.json()
    
    # Second request - should be the same
    response2 = await async_client.get("/sinhvien/hienthi/tatca")
    assert response2.status_code == 200
    data2 = response2.json()
    
    # Should have same data
    assert data1["result"] == data2["result"]
    assert len(data1["result"]) == len(data2["result"])

@pytest.mark.asyncio
async def test_seeded_data_integrity(async_client: AsyncClient):
    """Test that seeded data is correct"""
    # Test sinh vien
    response = await async_client.get("/sinhvien/hienthi/4")
    assert response.status_code == 200
    sinh_vien = response.json()["result"]
    assert sinh_vien["ten_sinh_vien"] == "Bao"
    assert sinh_vien["khoa"] == "Information Technology"
    
    # Test khoa
    response = await async_client.get("/faculty/display/name?name=Information Technology")
    assert response.status_code == 200
    khoa_list = response.json()["result"]
    assert len(khoa_list) >= 1
    assert khoa_list[0]["id"] == "K01"
    
    # Test lop hoc
    response = await async_client.get("/lophoc/lop/hienthi/tatca")
    assert response.status_code == 200
    lop_hoc_list = response.json()["result"]
    assert len(lop_hoc_list) >= 1
    assert lop_hoc_list[0]["id"] == "TEST001"
