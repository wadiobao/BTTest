import os
from urllib.parse import quote_plus
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import SQLModel

DB_USER = os.getenv("MYSQL_USER", "root")
DB_PASS = os.getenv("MYSQL_PASSWORD", "hellobao0X@")
DB_HOST = os.getenv("MYSQL_HOST", "localhost")  # Changed from localhost to db for Docker
DB_PORT = os.getenv("MYSQL_PORT", "3306")
DB_NAME = os.getenv("MYSQL_DATABASE", "quan_li_sinh_vien")

DATABASE_URL = f"mysql+aiomysql://{DB_USER}:{quote_plus(DB_PASS)}@{DB_HOST}:{DB_PORT}/quan_li_sinh_vien"

async_engine = create_async_engine(DATABASE_URL, echo=True)

async def create_db_and_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

async def get_session():
    from sqlmodel.ext.asyncio.session import AsyncSession
    async with AsyncSession(async_engine) as session:
        yield session 