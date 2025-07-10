import pytest
import pytest_asyncio
import asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlmodel import SQLModel
from datetime import date

from app.main import app
from app.database import get_session
# Import all models to ensure they are registered with SQLModel
from app.models.base_models.main_models import Khoa, SinhVien, LopHoc, SinhVienLopHoc

# --- 1. Database Setup for Testing ---
DATABASE_URL = "sqlite+aiosqlite:///./test.db"  # Using file-based SQLite for consistency

engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# --- 2. Dependency Override ---
async def override_get_session() -> AsyncSession:
    async with SessionLocal() as session:
        yield session

app.dependency_overrides[get_session] = override_get_session

# --- 3. Global Fixtures ---
@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()

@pytest_asyncio.fixture(scope="function", autouse=True)
async def setup_database():
    """Create, seed, and drop tables for each test function."""
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    
    # Seed test data
    async with SessionLocal() as session:
        # Create test Khoa
        khoa = Khoa(id="K01", ten_khoa="Information Technology")
        session.add(khoa)
        
        # Create test SinhVien
        sinh_vien = SinhVien(
            id=4,
            ten_sinh_vien="Bao",
            gioi_tinh="Nam",
            ngay_sinh=date(2000, 1, 1),
            sdt="0123456789",
            email="bao@example.com",
            que_quan="Hà Nội",
            khoa_id="K01"
        )
        session.add(sinh_vien)
        
        # Create test LopHoc
        lop_hoc = LopHoc(
            id="TEST001",
            ten_lop_hoc="Test Lop",
            si_so=30
        )
        session.add(lop_hoc)
        
        await session.commit()
    
    yield
    
    # Cleanup
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)

@pytest_asyncio.fixture(scope="function")
async def async_client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client
