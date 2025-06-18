import pytest
import pytest_asyncio
from sqlmodel.ext.asyncio.session import AsyncSession
from app.services.sinh_vien_service import SinhVienService
from app.repository.sinh_vien_repo import SinhVienRepo
from app.repository.khoa_repo import KhoaRepo
from app.database import async_engine
from app.models.sinh_vien_request import SinhVienRequest
import logging
from sqlalchemy import select
from app.models.base_models.main_models import SinhVien

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@pytest_asyncio.fixture
async def db_session():
    logger.info("Creating database session")
    async with AsyncSession(async_engine) as session:
        try:
            yield session
        finally:
            logger.info("Closing database session")
            await session.close()

@pytest_asyncio.fixture
async def sinh_vien_service(db_session):
    logger.info("Initializing SinhVienService with session")
    sinh_vien_repo = SinhVienRepo(db_session)
    khoa_repo = KhoaRepo(db_session)
    service = SinhVienService(sinh_vien_repo, khoa_repo)
    return service

sinh_vien_data = SinhVienRequest(
    ten_sinh_vien="Test Student",
    gioi_tinh="Nam",
    ngay_sinh="2000-01-01",
    sdt="0123456789",
    email="test@example.com",
    que_quan="Ha Noi",
    khoa_id="K02"
)

@pytest.mark.asyncio
async def test_them_sinh_vien(sinh_vien_service):
    try:
        sinh_vien_id = await sinh_vien_service.them_sinh_vien_db(sinh_vien_data)
        assert isinstance(sinh_vien_id, int)
        
        # Verify the student was created
        sinh_vien = await sinh_vien_service.hien_sinh_vien_id_db(sinh_vien_id)
        assert sinh_vien.ten_sinh_vien == sinh_vien_data.ten_sinh_vien
        assert sinh_vien.gioi_tinh == sinh_vien_data.gioi_tinh
        assert sinh_vien.ngay_sinh == sinh_vien_data.ngay_sinh
        assert sinh_vien.sdt == sinh_vien_data.sdt
        assert sinh_vien.email == sinh_vien_data.email
        assert sinh_vien.que_quan == sinh_vien_data.que_quan
        assert sinh_vien.khoa == 'Toán'
    except Exception as e:
        pytest.fail(f"Test failed with exception: {str(e)}")

@pytest.mark.asyncio
async def test_hien_ds_sinh_vien(sinh_vien_service):
    try:
        # First add a test student
        await sinh_vien_service.them_sinh_vien_db(sinh_vien_data)
        
        # Then test getting all students
        ds_sinh_vien = await sinh_vien_service.hien_ds_sinh_vien_db()
        assert isinstance(ds_sinh_vien, list)
        assert len(ds_sinh_vien) > 0
    except Exception as e:
        pytest.fail(f"Test failed with exception: {str(e)}")

@pytest.mark.asyncio
async def test_hien_sinh_vien_theo_id(sinh_vien_service):
    try:
        # First add a test student
        sinh_vien_id = await sinh_vien_service.them_sinh_vien_db(sinh_vien_data)
        
        # Then test getting by ID
        sinh_vien = await sinh_vien_service.hien_sinh_vien_id_db(sinh_vien_id)
        assert sinh_vien.ten_sinh_vien == sinh_vien_data.ten_sinh_vien
    except Exception as e:
        pytest.fail(f"Test failed with exception: {str(e)}")

@pytest.mark.asyncio
async def test_cap_nhat_sinh_vien(sinh_vien_service):
    try:
        # First add a test student
        sinh_vien_id = await sinh_vien_service.them_sinh_vien_db(sinh_vien_data)
        
        # Then update
        update_data = sinh_vien_data.copy()
        update_data.ten_sinh_vien = "Updated Student"
        
        sinh_vien = await sinh_vien_service.cap_nhat_sinh_vien_db(sinh_vien_id, update_data)
        assert sinh_vien.ten_sinh_vien == update_data.ten_sinh_vien
    except Exception as e:
        pytest.fail(f"Test failed with exception: {str(e)}")

@pytest.mark.asyncio
async def test_xoa_sinh_vien(sinh_vien_service):
    try:
        # First add a test student
        sinh_vien_id = await sinh_vien_service.them_sinh_vien_db(sinh_vien_data)
        
        # Then delete
        result = await sinh_vien_service.xoa_sinh_vien_db(sinh_vien_id)
        assert result is True
        
        # Verify it's deleted
        try:
            await sinh_vien_service.hien_sinh_vien_id_db(sinh_vien_id)
            pytest.fail("Student should be deleted")
        except Exception:
            pass
    except Exception as e:
        pytest.fail(f"Test failed with exception: {str(e)}")