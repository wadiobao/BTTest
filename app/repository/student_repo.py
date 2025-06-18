from typing import List, Optional
from datetime import datetime
from sqlalchemy import extract, select
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import selectinload
from sqlmodel import select
from sqlalchemy.exc import IntegrityError

from app.models.base_models import Faculty, Student, Classes
from app.repository.i_student_repo import IStudentRepo


class StudentRepo(IStudentRepo):
    """Implementation of student repository"""
    
    def __init__(self, session: AsyncSession):
        self.session = session
        
    async def check_existed(self, id: int) -> bool:
        query = select(Student).where(Student.id == id).exists()
        result = await self.session.execute(select(query))
        return result.scalar()
    
    async def add(self, student: Student) -> int:
        self.session.add(student)
        await self.session.commit()
        await self.session.refresh(student)
        return student.id
    
    async def display(self) -> List[Student]:
        result = await self.session.execute(
            select(Student)
            .options(
                selectinload(Student.faculty),
                selectinload(Student.classes)
            )
        )
        return result.scalars().all()
    
    async def display_by_age_asc(self) -> List[Student]:
        current_year = datetime.now().year
        stmt = (
            select(Student)
            .options(
                selectinload(Student.faculty),
                selectinload(Student.classes)
            )
        ).order_by((extract('year', Student.birth_date)-current_year).asc())
        
        result = await self.session.execute(stmt)
        return result.scalars().all()
    
    async def display_by_age_desc(self) -> List[Student]:
        current_year = datetime.now().year
        stmt = (
            select(Student)
            .options(
                selectinload(Student.faculty),
                selectinload(Student.classes)
            )
        ).order_by((extract('year', Student.birth_date)-current_year).desc())
        
        result = await self.session.execute(stmt)
        return result.scalars().all()
    
    async def display_by_name(self, name: str) -> List[Student]:
        stmt = (
            select(Student)
            .options(
                selectinload(Student.faculty),
                selectinload(Student.classes)
            )
        ).where(Student.name.like(f"%{name}%"))
        
        result = await self.session.execute(stmt)
        return result.scalars().all()
    
    async def display_by_id(self, id: int) -> Student:
        stmt = (
            select(Student)
            .options(
                selectinload(Student.faculty),
                selectinload(Student.classes)
            )
        ).where(Student.id == id)
        
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
    
    async def update(self, id: int, student_data: dict) -> int:
        student = await self.session.get(Student, id)
        for key, value in student_data.items():
            setattr(student, key, value)
        self.session.add(student)
        await self.session.commit()
        await self.session.refresh(student)
        return student.id
    
    async def delete(self, id: int) -> int:
        stmt = (
            select(Student)
            .options(
                selectinload(Student.classes),
                selectinload(Student.faculty)
            )
        ).where(Student.id == id)
        result = await self.session.execute(stmt)
        student = result.scalar_one_or_none()
        
        if student is None:
            return None
        student.classes = []
        student.faculty = None
        await self.session.delete(student)
        await self.session.commit()
        return id 