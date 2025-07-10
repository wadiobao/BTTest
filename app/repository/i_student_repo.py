from abc import ABC, abstractmethod
from typing import List, Optional
from app.models.base_models import Student

class IStudentRepo(ABC):
    """Interface for student repository operations"""
    
    @abstractmethod
    async def check_existed(self, id: int) -> bool:
        """Check if student exists by ID"""
        pass
    
    @abstractmethod
    async def add(self, student: Student) -> int:
        """Add new student"""
        pass
    
    @abstractmethod
    async def display(self) -> List[Student]:
        """Get all students"""
        pass
    
    @abstractmethod
    async def update(self, id: int, student_data: dict) -> int:
        """Update student by ID"""
        pass
    
    @abstractmethod
    async def display_by_age_asc(self) -> List[Student]:
        """Get students sorted by age ascending"""
        pass
    
    @abstractmethod
    async def display_by_age_desc(self) -> List[Student]:
        """Get students sorted by age descending"""
        pass
    
    @abstractmethod
    async def display_by_name(self, name: str) -> List[Student]:
        """Get students by name"""
        pass
    
    @abstractmethod
    async def display_by_id(self, id: int) -> Student:
        """Get student by ID"""
        pass
    
    @abstractmethod
    async def delete(self, id: int) -> int:
        """Delete student by ID"""
        pass 
