from typing import List, Optional
from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import selectinload, joinedload
from sqlmodel import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy import extract
from datetime import datetime

from app.database import get_session
from app.exceptions import ResponseException
from app.models.base_models import Faculty, Student, Classes
from app.models.response_models import StudentResponse
from app.utils.mapper import map_sinhvien_to_response
from app.repository.student_repo import StudentRepo
from app.repository.faculty_repo import FacultyRepo
from app.models.request_models.student_request import StudentRequest

class StudentService:
    """Service class for student operations"""
    
    def __init__(self, student_repo: StudentRepo, faculty_repo: FacultyRepo):
        self.student_repo = student_repo
        self.faculty_repo = faculty_repo
    
    async def create_student(self, student_request: StudentRequest) -> Optional[StudentResponse]:
        """Create a new student"""
        faculty_existed = await self.faculty_repo.check_existed(student_request.faculty_id)
        if not faculty_existed:
            raise ResponseException(
                message="Faculty does not exist")
            
        student = Student.from_orm(student_request)
        result = await self.student_repo.add(student)
        return result
    
    async def get_all_students(self) -> Optional[List[StudentResponse]]:
        """Get all students"""
        student_list = await self.student_repo.display()
        student_responses = [map_sinhvien_to_response(sv) for sv in student_list]
        return student_responses
    
    async def get_students_by_age(self, order: str) -> Optional[List[StudentResponse]]:
        """Get students sorted by age"""
        if order == "desc":
            student_list = await self.student_repo.display_by_age_desc()
        else:
            student_list = await self.student_repo.display_by_age_asc()
            
        student_responses = [map_sinhvien_to_response(sv) for sv in student_list]
        return student_responses
    
    async def get_student_by_id(self, id: int) -> Optional[StudentResponse]:
        """Get student by ID"""
        student = await self.student_repo.display_by_id(id)
        if not student:
            raise ResponseException(
                message="Student does not exist")
        student_response = map_sinhvien_to_response(student)
        return student_response
    
    async def get_students_by_name(self, name: str) -> Optional[List[StudentResponse]]:    
        """Get students by name"""
        student_list = await self.student_repo.display_by_name(name)
        if not student_list:
            raise ResponseException(
                message="Student does not exist")
        
        student_responses = [map_sinhvien_to_response(sv) for sv in student_list]
        return student_responses
    
    async def update_student(self, id: int, student_request: StudentRequest) -> Optional[StudentResponse]:
        """Update student by ID"""
        faculty_existed = await self.faculty_repo.check_existed(student_request.faculty_id)
        if not faculty_existed:
            raise ResponseException(
                message="Faculty does not exist")
            
        student = await self.student_repo.check_existed(id)
        if not student:
            raise ResponseException(
                message="Student does not exist")
            
        student_data = student_request.model_dump(exclude_unset=True)
        await self.student_repo.update(id, student_data)
        # Get the updated student object
        updated_student = await self.student_repo.display_by_id(id)
        student_response = map_sinhvien_to_response(updated_student)
        return student_response
    
    async def delete_student(self, id: int) -> Optional[StudentResponse]:
        """Delete student by ID"""
        student_existed = await self.student_repo.check_existed(id)
        if not student_existed:
            raise ResponseException(
                message="Student does not exist")
        
        return await self.student_repo.delete(id) 