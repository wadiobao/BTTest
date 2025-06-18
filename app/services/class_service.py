from typing import List, Optional
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from app.exceptions import ResponseException
from app.models.base_models import Faculty, Student, Classes
from app.models.request_models.class_request import ClassRequest
from app.models.response_models import ClassResponse
from app.utils.mapper import map_lop_hoc_to_response
from app.repository.class_repo import ClassRepo


class ClassService:
    """Service class for class operations"""
    
    def __init__(self, repo: ClassRepo):
        self.repo = repo

    async def create_class(self, class_request: ClassRequest):
        """Create a new class"""
        try:
            class_obj = Classes(
                id=class_request.id,
                name=class_request.name,
                capacity=class_request.capacity
            )
            class_obj = await self.repo.add(class_obj)
            return map_lop_hoc_to_response(class_obj)
        except IntegrityError as e:
            if "Duplicate entry" in str(e):
                raise ResponseException(
                    message=f"Class with ID '{class_request.id}' already exists")
            raise ResponseException(
                message="An error occurred while creating the class")

    async def get_all_classes(self):
        """Get all classes"""
        class_list = await self.repo.get_all()
        return [map_lop_hoc_to_response(class_obj) for class_obj in class_list]

    async def get_class_by_id(self, id: str):
        """Get class by ID"""
        class_obj = await self.repo.get_by_id(id)
        if not class_obj:
            raise ResponseException(
                message=f"Class with ID '{id}' not found")
        return map_lop_hoc_to_response(class_obj)

    async def update_class(self, id: str, class_request: ClassRequest):
        """Update class by ID"""
        class_obj = await self.repo.get_by_id(id)
        if not class_obj:
            raise ResponseException(
                message=f"Class with ID '{id}' not found")
        try:
            class_data = class_request.model_dump(exclude_unset=True)
            class_obj = await self.repo.update(id, class_data)
            return map_lop_hoc_to_response(class_obj)
        except IntegrityError as e:
            raise ResponseException(
                message="An error occurred while updating the class")

    async def delete_class(self, id: str):
        """Delete class by ID"""
        class_obj = await self.repo.get_by_id(id)
        if not class_obj:
            raise ResponseException(
                message=f"Class with ID '{id}' not found")
        try:
            success = await self.repo.delete(id)
            if not success:
                raise ResponseException(
                    message="Cannot delete class because there are students referencing this class")
            return True
        except IntegrityError as e:
            raise ResponseException(
                message="Cannot delete class because there are students referencing this class") 