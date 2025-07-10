from datetime import datetime
from typing import List, Optional, Dict
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.base_models import Faculty, Student, Classes
from app.repository.class_repo.i_class_repo import IClassRepo


class ClassRepo(IClassRepo):
    """Implementation of class repository"""
    
    def __init__(self, session: AsyncSession):
        self.session = session

    async def check_existed(self, id: str) -> bool:
        query = select(Classes).where(Classes.id == id).where(Classes.deleted_at==None).exists()
        result = await self.session.execute(select(query))
        return result.scalar()

    async def get_all(self) -> List[Classes]:
        statement = (
            select(Classes)
            .where(Classes.deleted_at==None)
            .options(
                selectinload(Classes.students)
            )
        )
        result = await self.session.execute(statement)
        return result.scalars().all()

    async def get_by_id(self, id: str) -> Optional[Classes]:
        statement = (
            select(Classes)
            .where(Classes.id == id)
            .where(Classes.deleted_at==None)
            .options(
                selectinload(Classes.students)
            )
        )
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def add(self, class_obj: Classes) -> Classes:
        self.session.add(class_obj)
        await self.session.commit()
        await self.session.refresh(class_obj)
        return class_obj

    async def update(self, id: str, class_data: Dict) -> Optional[Classes]:
        stmt = (
            select(Classes)
            .where(Classes.deleted_at==None)
            .options(
                selectinload(Classes.students)
            )
        ).where(Classes.id == id)       
        result = await self.session.execute(stmt)
        class_obj = result.scalar_one_or_none()
        if not class_obj:
            return None

        for key, value in class_data.items():
            setattr(class_obj, key, value)

        await self.session.commit()
        await self.session.refresh(class_obj)
        return class_obj

    async def delete(self, id: str) -> Optional[bool]:
        stmt = (
            select(Classes)
            .where(Classes.deleted_at==None)
            .options(
                selectinload(Classes.students)
            )
        ).where(Classes.id == id)       
        result = await self.session.execute(stmt)
        class_obj = result.scalar_one_or_none()
        if not class_obj:
            return False

        class_obj.deleted_at = datetime.utcnow()
        await self.session.commit()
        return True 
