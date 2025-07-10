import pytest
import pytest_asyncio
from sqlmodel.ext.asyncio.session import AsyncSession
from app.services.student_service import StudentService
from app.repository.student_repo.student_repo import StudentRepo
from app.repository.faculty_repo.faculty_repo import FacultyRepo
from app.database import async_engine
from app.models.request_models.student_request import StudentRequest
import logging
from sqlalchemy import select
from app.models.base_models.student import Student

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
async def student_service(db_session):
    logger.info("Initializing StudentService with session")
    student_repo = StudentRepo(db_session)
    faculty_repo = FacultyRepo(db_session)
    service = StudentService(student_repo, faculty_repo)
    return service

student_data = StudentRequest(
    ten_student="Test Student",
    gioi_tinh="Nam",
    ngay_sinh="2000-01-01",
    sdt="0123456789",
    email="test@example.com",
    que_quan="Ha Noi",
    faculty_id="K02"
)

@pytest.mark.asyncio
async def test_create_student(student_service):
    try:
        student_id = await student_service.them_student_db(student_data)
        assert isinstance(student_id, int)
        
        # Verify the student was created
        student = await student_service.hien_student_id_db(student_id)
        assert student.ten_student == student_data.ten_student
        assert student.gioi_tinh == student_data.gioi_tinh
        assert student.ngay_sinh == student_data.ngay_sinh
        assert student.sdt == student_data.sdt
        assert student.email == student_data.email
        assert student.que_quan == student_data.que_quan
        assert student.faculty == 'Mathematics'
    except Exception as e:
        pytest.fail(f"Test failed with exception: {str(e)}")

@pytest.mark.asyncio
async def test_list_students(student_service):
    try:
        # First add a test student
        await student_service.them_student_db(student_data)
        
        # Then test getting all students
        ds_student = await student_service.hien_ds_student_db()
        assert isinstance(ds_student, list)
        assert len(ds_student) > 0
    except Exception as e:
        pytest.fail(f"Test failed with exception: {str(e)}")

@pytest.mark.asyncio
async def test_get_student_by_id(student_service):
    try:
        # First add a test student
        student_id = await student_service.them_student_db(student_data)
        
        # Then test getting by ID
        student = await student_service.hien_student_id_db(student_id)
        assert student.ten_student == student_data.ten_student
    except Exception as e:
        pytest.fail(f"Test failed with exception: {str(e)}")

@pytest.mark.asyncio
async def test_update_student(student_service):
    try:
        # First add a test student
        student_id = await student_service.them_student_db(student_data)
        
        # Then update
        update_data = student_data.copy()
        update_data.ten_student = "Updated Student"
        
        student = await student_service.cap_nhat_student_db(student_id, update_data)
        assert student.ten_student == update_data.ten_student
    except Exception as e:
        pytest.fail(f"Test failed with exception: {str(e)}")

@pytest.mark.asyncio
async def test_delete_student(student_service):
    try:
        # First add a test student
        student_id = await student_service.them_student_db(student_data)
        
        # Then delete
        result = await student_service.xoa_student_db(student_id)
        assert result is True
        
        # Verify it's deleted
        try:
            await student_service.hien_student_id_db(student_id)
            pytest.fail("Student should be deleted")
        except Exception:
            pass
    except Exception as e:
        pytest.fail(f"Test failed with exception: {str(e)}")
