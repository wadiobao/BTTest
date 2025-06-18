import pytest
import pytest_asyncio
from httpx import AsyncClient

# --- Test Cases ---
@pytest.mark.asyncio
async def test_them_sinh_vien_thanh_cong(async_client: AsyncClient):
    sinh_vien_data = {
        "ten_sinh_vien": "Student Moi",
        "gioi_tinh": "Nữ",
        "ngay_sinh": "2001-02-03",
        "sdt": "0974745448",
        "email": "moi@example.com",
        "que_quan": "Da Nang",
        "khoa_id": "K01"
    }
    response = await async_client.post("/sinhvien/them/", json=sinh_vien_data)
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == 200
    created_id = data["result"]
    # Verify by GET
    get_response = await async_client.get(f"/sinhvien/hienthi/{created_id}")
    assert get_response.status_code == 200
    result = get_response.json()["result"]
    assert result["ten_sinh_vien"] == sinh_vien_data["ten_sinh_vien"]
    assert result["khoa"] == "Công nghệ thông tin"

@pytest.mark.asyncio
async def test_them_sinh_vien_khong_thanh_cong(async_client: AsyncClient):
    sinh_vien_data = {
        "ten_sinh_vien": "Student Moi",
        "gioi_tinh": "N",
        "ngay_sinh": "2001-02-03",
        "sdt": "097",
        "email": "moi@example.com",
        "que_quan": "Da Nang",
        "khoa_id": "K01"
    }
    response = await async_client.post("/sinhvien/them/", json=sinh_vien_data)
    assert response.status_code == 417
    data = response.json()
    assert data["code"] == 422
    result = data["result"]
    assert isinstance(result,str)
    
@pytest.mark.asyncio
async def test_hien_ds_sinh_vien_sau_khi_them(async_client: AsyncClient):
    response = await async_client.get("/sinhvien/hienthi/tatca")
    assert response.status_code == 200
    data = response.json()
    assert len(data["result"]) >= 1

@pytest.mark.asyncio
async def test_hien_sinh_vien_theo_id(async_client: AsyncClient):
    response = await async_client.get("/sinhvien/hienthi/4")
    assert response.status_code == 200
    data = response.json()
    assert data["result"]["ten_sinh_vien"] == "Bao"

@pytest.mark.asyncio
async def test_hien_sinh_vien_theo_ten(async_client: AsyncClient):
    response = await async_client.get("/sinhvien/hienthi/ten?ten=Bao")
    assert response.status_code == 200
    data = response.json()
    assert len(data["result"]) >= 1
    assert data["result"][0]["ten_sinh_vien"] == "Bao"

@pytest.mark.asyncio
async def test_sua_sinh_vien(async_client: AsyncClient):
    # Need to provide all required fields for update
    update_data = {
        "ten_sinh_vien": "Ten Da Duoc Cap Nhat",
        "gioi_tinh": "Nam",
        "ngay_sinh": "2000-01-01",
        "sdt": "0123456789",
        "email": "bao@example.com",
        "que_quan": "Hà Nội",
        "khoa_id": "K01"
    }
    response = await async_client.patch("/sinhvien/sinhvien/sua/4", json=update_data)
    assert response.status_code == 200
    data = response.json()
    # data["result"] is a SinhVienResponse object, not an id
    result = data["result"]
    assert result["ten_sinh_vien"] == "Ten Da Duoc Cap Nhat"
    assert result["email"] == "bao@example.com"
    # Verify by GET using the id from the response
    updated_id = result["id"]
    get_response = await async_client.get(f"/sinhvien/hienthi/{updated_id}")
    assert get_response.status_code == 200
    get_result = get_response.json()["result"]
    assert get_result["ten_sinh_vien"] == "Ten Da Duoc Cap Nhat"
    assert get_result["email"] == "bao@example.com"

@pytest.mark.asyncio
async def test_xoa_sinh_vien(async_client: AsyncClient):
    # First create a new sinh vien to delete
    sinh_vien_data = {
        "ten_sinh_vien": "Sinh Vien De Xoa",
        "gioi_tinh": "Nam",
        "ngay_sinh": "2000-01-01",
        "sdt": "0987654321",
        "email": "xoa@example.com",
        "que_quan": "Ha Noi",
        "khoa_id": "K01"
    }
    create_response = await async_client.post("/sinhvien/them/", json=sinh_vien_data)
    assert create_response.status_code == 200
    created_id = create_response.json()["result"]
    # Now delete it
    response = await async_client.delete(f"/sinhvien/sinhvien/xoa/?id={created_id}")
    assert response.status_code == 200
    assert response.json()["code"] == 200
    # Verify it's deleted - expect exception or 404
    try:
        get_response = await async_client.get(f"/sinhvien/hienthi/{created_id}")
        # If no exception, should be 404
        assert get_response.status_code == 404
    except Exception as e:
        # If exception occurs, should contain "không tồn tại"
        assert "không tồn tại" in str(e)