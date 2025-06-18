from typing import List, Optional, Dict
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.main_models import LopHoc, SinhVien
from app.repository.i_lop_hoc_repo import ILopHocRepo


class LopHocRepo(ILopHocRepo):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def check_existed(self, id: str) -> bool:
        statement = select(LopHoc).where(LopHoc.id == id)
        result = await self.session.execute(statement)
        return result.scalar_one_or_none() is not None

    async def get_all(self) -> List[LopHoc]:
        statement = (
            select(LopHoc)
            .options(
                selectinload(LopHoc.ds_sinh_vien)
            )
        )
        result = await self.session.execute(statement)
        return result.scalars().all()

    async def get_by_id(self, id: str) -> Optional[LopHoc]:
        statement = (
            select(LopHoc)
            .where(LopHoc.id == id)
            .options(
                selectinload(LopHoc.ds_sinh_vien)
            )
        )
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def add(self, lop_hoc: LopHoc) -> LopHoc:
        self.session.add(lop_hoc)
        await self.session.commit()
        await self.session.refresh(lop_hoc)
        return lop_hoc

    async def update(self, id: str, lop_hoc_data: Dict) -> Optional[LopHoc]:
        lop_hoc = await self.get_by_id(id)
        if not lop_hoc:
            return None

        for key, value in lop_hoc_data.items():
            setattr(lop_hoc, key, value)

        await self.session.commit()
        await self.session.refresh(lop_hoc)
        return lop_hoc

    async def delete(self, id: str) -> bool:
        lop_hoc = await self.get_by_id(id)
        if not lop_hoc:
            return False

        await self.session.delete(lop_hoc)
        await self.session.commit()
        return True 