from datetime import datetime
from typing import List, Optional
from sqlalchemy import extract, select
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.main_models import Khoa, SinhVien
from app.repository.i_khoa_repo import IKhoaRepo


class KhoaRepo(IKhoaRepo):
    
    def __init__(self, session: AsyncSession):
        self.session = session
        
    async def check_existed(self, id: str) -> bool:
        query = select(Khoa).where(Khoa.id == id).exists()
        result = await self.session.execute(select(query))
        return result.scalar()

    async def get_all(self) -> List[Khoa]:
        statement = (
            select(Khoa)
            .options(
                selectinload(Khoa.ds_sinh_vien).selectinload(SinhVien.ds_lop_hoc)
            )
        )
        result = await self.session.execute(statement)
        return result.scalars().all()

    async def get_by_id(self, id: str) -> Optional[Khoa]:
        statement = (
            select(Khoa)
            .where(Khoa.id == id)
            .options(
                selectinload(Khoa.ds_sinh_vien).selectinload(SinhVien.ds_lop_hoc)
            )
        )
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def add(self, khoa: Khoa) -> Khoa:
        self.session.add(khoa)
        await self.session.commit()
        await self.session.refresh(khoa)
        return khoa

    async def update(self, id: str, khoa_data: dict) -> Optional[Khoa]:
        khoa = await self.get_by_id(id)
        if khoa:
            for key, value in khoa_data.items():
                setattr(khoa, key, value)
            await self.session.commit()
            await self.session.refresh(khoa)
        return khoa

    async def delete(self, id: str) -> bool:
        khoa = await self.get_by_id(id)
        if khoa:
            await self.session.delete(khoa)
            await self.session.commit()
            return True
        return False