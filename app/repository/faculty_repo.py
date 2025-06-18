from typing import List, Optional, Dict
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import selectinload
from sqlmodel import select
from sqlalchemy.exc import IntegrityError

from app.models.base_models import Faculty, Student, Classes
from app.repository.i_faculty_repo import IFacultyRepo


class FacultyRepo(IFacultyRepo):
    """Implementation of faculty repository"""
    
    def __init__(self, session: AsyncSession):
        self.session = session
        
    async def check_existed(self, id: str) -> bool:
        query = select(Faculty).where(Faculty.id == id).exists()
        result = await self.session.execute(select(query))
        return result.scalar()
    
    async def get_all(self) -> List[Faculty]:
        statement = (
            select(Faculty)
            .options(
                selectinload(Faculty.students).selectinload(Student.classes)
            )
        )
        result = await self.session.execute(statement)
        return result.scalars().all()

    async def get_by_id(self, id: str) -> Optional[Faculty]:
        statement = (
            select(Faculty)
            .where(Faculty.id == id)
            .options(
                selectinload(Faculty.students).selectinload(Student.classes)
            )
        )
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def add(self, faculty: Faculty) -> Faculty:
        self.session.add(faculty)
        await self.session.commit()
        await self.session.refresh(faculty)
        return faculty

    async def update(self, id: str, faculty_data: Dict) -> Optional[Faculty]:
        faculty = await self.get_by_id(id)
        if faculty:
            for key, value in faculty_data.items():
                setattr(faculty, key, value)
            await self.session.commit()
            await self.session.refresh(faculty)
        return faculty

    async def delete(self, id: str) -> bool:
        faculty = await self.get_by_id(id)
        if not faculty:
            return False
        await self.session.delete(faculty)
        await self.session.commit()
        return True 