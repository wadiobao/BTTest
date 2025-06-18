from abc import ABC, abstractmethod
from typing import List, Optional, Dict

from app.models.main_models import Khoa

class IKhoaRepo(ABC):
    
    @abstractmethod
    async def check_existed(self, id: str) -> bool:
        pass

    @abstractmethod
    async def get_all(self) -> List[Khoa]:
        pass

    @abstractmethod
    async def get_by_id(self, id: str) -> Optional[Khoa]:
        pass

    @abstractmethod
    async def add(self, khoa: Khoa) -> Khoa:
        pass

    @abstractmethod
    async def update(self, id: str, khoa_data: Dict) -> Optional[Khoa]:
        pass

    @abstractmethod
    async def delete(self, id: str) -> bool:
        pass

