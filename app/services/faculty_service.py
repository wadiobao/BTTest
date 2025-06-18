from typing import List, Optional
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import selectinload, joinedload
from sqlmodel import select
from sqlalchemy.exc import IntegrityError

from app.exceptions import ResponseException
from app.models.base_models import Faculty
from app.utils.mapper import map_khoa_to_response
from app.repository.faculty_repo import FacultyRepo
from app.models.request_models.faculty_request import FacultyRequest


class FacultyService:
    """Service class for faculty operations"""
    
    def __init__(self, repo: FacultyRepo):
        self.repo = repo

    async def create_faculty(self, faculty_request: FacultyRequest):
        """Create a new faculty"""
        try:
            faculty = Faculty(
                id=faculty_request.id,
                name=faculty_request.name
            )
            faculty = await self.repo.add(faculty)
            await self.repo.session.commit()
            await self.repo.session.refresh(faculty)
            # Load relationships to avoid MissingGreenlet error
            await self.repo.session.refresh(faculty, attribute_names=['students'])
            return map_khoa_to_response(faculty)
        except IntegrityError as e:
            if "Duplicate entry" in str(e):
                raise ResponseException(
                    message=f"Faculty with ID '{faculty_request.id}' already exists")
            raise ResponseException(
                message="An error occurred while creating the faculty")

    async def get_all_faculties(self):
        """Get all faculties"""
        faculty_list = await self.repo.get_all()
        return [map_khoa_to_response(faculty) for faculty in faculty_list]

    async def get_faculty_by_id(self, id: str):
        """Get faculty by ID"""
        faculty = await self.repo.get_by_id(id)
        if not faculty:
            raise ResponseException(
                message=f"Faculty with ID '{id}' not found")
        return map_khoa_to_response(faculty)

    async def get_faculty_by_name(self, name: str):
        """Get faculty by name"""
        # This method needs to be implemented in the repository
        # For now, we'll get all faculties and filter by name
        faculty_list = await self.repo.get_all()
        for faculty in faculty_list:
            if faculty.name.lower() == name.lower():
                return map_khoa_to_response(faculty)
        raise ResponseException(
            message=f"Faculty with name '{name}' not found")

    async def update_faculty(self, id: str, faculty_request: FacultyRequest):
        """Update faculty by ID"""
        faculty = await self.repo.get_by_id(id)
        if not faculty:
            raise ResponseException(
                message=f"Faculty with ID '{id}' not found")
        try:
            faculty_data = faculty_request.model_dump(exclude_unset=True)
            faculty = await self.repo.update(id, faculty_data)
            return map_khoa_to_response(faculty)
        except IntegrityError as e:
            raise ResponseException(
                message="An error occurred while updating the faculty")

    async def delete_faculty(self, id: str):
        """Delete faculty by ID"""
        faculty = await self.repo.get_by_id(id)
        if not faculty:
            raise ResponseException(
                message=f"Faculty with ID '{id}' not found")
        try:
            success = await self.repo.delete(id)
            if not success:
                raise ResponseException(
                    message="Cannot delete faculty because there are students referencing this faculty")
            return True
        except IntegrityError as e:
            raise ResponseException(
                message="Cannot delete faculty because there are students referencing this faculty") 