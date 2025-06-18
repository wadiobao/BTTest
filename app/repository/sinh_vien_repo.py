from datetime import datetime
from typing import Any, List
from sqlalchemy import extract, select
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.main_models import SinhVien
from app.repository.i_sinh_vien_repo import ISinhVienRepo

    
class SinhVienRepo(ISinhVienRepo):
    
    def __init__(self, session:AsyncSession):
        self.session = session
        
    async def check_existed(self,id:int) -> bool:
        query = select(SinhVien).where(SinhVien.id == id).exists()
        result = await self.session.execute(select(query))
        return result.scalar()
    
    async def add(self,sinhVien: SinhVien) -> int:
        self.session.add(sinhVien)
        await self.session.commit()
        await self.session.refresh(sinhVien)
        return sinhVien.id
    
    async def display(self) -> List[SinhVien]:
        result = await self.session.execute(
            select(SinhVien)
            .options(
                selectinload(SinhVien.khoa),
                selectinload(SinhVien.ds_lop_hoc)
            )
        )
        return result.scalars().all()
    
    async def display_by_age_asc(self)-> List[SinhVien]:
        current_year = datetime.now().year
        stmt = (
            select(SinhVien)
            .options(
                selectinload(SinhVien.khoa),
                selectinload(SinhVien.ds_lop_hoc)
            )
        ).order_by((extract('year', SinhVien.ngay_sinh)-current_year).asc())
        
        result = await self.session.execute(stmt)
        return result.scalars().all()
    
    async def display_by_age_desc(self)-> List[SinhVien]:
        current_year = datetime.now().year
        stmt = (
            select(SinhVien)
            .options(
                selectinload(SinhVien.khoa),
                selectinload(SinhVien.ds_lop_hoc)
            )
        ).order_by((extract('year', SinhVien.ngay_sinh)-current_year).desc())
        
        result = await self.session.execute(stmt)
        return result.scalars().all()
    
    async def display_by_name(self,ten:str)-> List[SinhVien]:
        stmt = (
            select(SinhVien)
            .options(
                selectinload(SinhVien.khoa),
                selectinload(SinhVien.ds_lop_hoc)
            )
        ).where(SinhVien.ten_sinh_vien.like(f"%{ten}%"))
        
        result = await self.session.execute(stmt)
        return result.scalars().all()
    
    async def display_by_id(self,id:int)-> SinhVien:
        stmt = (
            select(SinhVien)
            .options(
                selectinload(SinhVien.khoa),
                selectinload(SinhVien.ds_lop_hoc)
            )
        ).where(SinhVien.id==id)
        
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
    
    async def update(self,id:int,sinhVien_data:SinhVien) -> int:
        sinhVien = await self.session.get(SinhVien,id)
        sinhVien.sqlmodel_update(sinhVien_data)
        self.session.add(sinhVien)
        await self.session.commit()
        await self.session.refresh(sinhVien) 
        return id
    
    async def delete(self,id:int) -> int:
        stmt = (
            select(SinhVien)
            .options(
                selectinload(SinhVien.ds_lop_hoc),
                selectinload(SinhVien.khoa)
            )
        ).where(SinhVien.id == id)
        result = await self.session.execute(stmt)
        sinhVien = result.scalar_one_or_none()
        if sinhVien is None:
            return None
        sinhVien.ds_lop_hoc = []
        sinhVien.khoa = None
        await self.session.delete(sinhVien)
        await self.session.commit()
        return id