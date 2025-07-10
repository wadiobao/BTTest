from abc import ABC, abstractmethod
from typing import List, Optional, Dict
from app.models.base_models import Faculty

class IFacultyRepo(ABC):
    """Interface for faculty repository operations"""
    
    @abstractmethod
    async def check_existed(self, id: str) -> bool:
        """Check if faculty exists by ID"""
        pass
    
    @abstractmethod
    async def get_all(self) -> List[Faculty]:
        """Get all faculties"""
        pass
    
    @abstractmethod
    async def get_by_id(self, id: str) -> Optional[Faculty]:
        """Get faculty by ID"""
        pass
    
    @abstractmethod
    async def add(self, faculty: Faculty) -> Faculty:
        """Add new faculty"""
        pass
    
    @abstractmethod
    async def update(self, id: str, faculty_data: Dict) -> Optional[Faculty]:
        """Update faculty by ID"""
        pass
    
    @abstractmethod
    async def delete(self, id: str) -> bool:
        """Delete faculty by ID"""
        pass 
