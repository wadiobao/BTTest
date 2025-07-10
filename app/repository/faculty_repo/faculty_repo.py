from datetime import datetime
from typing import List, Optional, Dict
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import selectinload
from sqlmodel import select
from sqlalchemy.exc import IntegrityError

from app.models.base_models import Faculty, Student, Classes
from app.repository.faculty_repo.i_faculty_repo import IFacultyRepo


class FacultyRepo(IFacultyRepo):
    """Implementation of faculty repository"""
    
    def __init__(self, session: AsyncSession):
        self.session = session
        
    async def check_existed(self, id: str) -> bool:
        query = select(Faculty).where(Faculty.id == id).where(Faculty.deleted_at==None).exists()
        result = await self.session.execute(select(query))
        return result.scalar()
    
    async def get_all(self) -> List[Faculty]:
        statement = (
            select(Faculty)
            .where(Faculty.deleted_at==None)
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
            .where(Faculty.deleted_at==None)
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
        statement = (
            select(Faculty)
            .where(Faculty.id == id)
            .where(Faculty.deleted_at==None)
            .options(
                selectinload(Faculty.students).selectinload(Student.classes)
            )
        )        
        result = await self.session.execute(statement)
        faculty = result.scalar_one_or_none()
        if faculty:
            for key, value in faculty_data.items():
                setattr(faculty, key, value)
            await self.session.commit()
            await self.session.refresh(faculty)
        return faculty

    async def delete(self, id: str) -> Optional[bool]:
        statement = (
            select(Faculty)
            .where(Faculty.id == id)
            .where(Faculty.deleted_at==None)
            .options(
                selectinload(Faculty.students).selectinload(Student.classes)
            )
        )
        result = await self.session.execute(statement)
        faculty = result.scalar_one_or_none()
        if not faculty:
            return False
        faculty.deleted_at = datetime.utcnow()
        await self.session.commit()
        return True 
