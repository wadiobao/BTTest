from abc import ABC, abstractmethod
from typing import List, Optional, Dict
from app.models.base_models import Classes

class IClassRepo(ABC):
    """Interface for class repository operations"""
    
    @abstractmethod
    async def check_existed(self, id: str) -> bool:
        """Check if class exists by ID"""
        pass

    @abstractmethod
    async def get_all(self) -> List[Classes]:
        """Get all classes"""
        pass

    @abstractmethod
    async def get_by_id(self, id: str) -> Optional[Classes]:
        """Get class by ID"""
        pass

    @abstractmethod
    async def add(self, class_obj: Classes) -> Classes:
        """Add new class"""
        pass

    @abstractmethod
    async def update(self, id: str, class_data: Dict) -> Optional[Classes]:
        """Update class by ID"""
        pass

    @abstractmethod
    async def delete(self, id: str) -> bool:
        """Delete class by ID"""
        pass 
