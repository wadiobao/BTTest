from abc import ABC, abstractmethod
from typing import List, Optional, Dict
from app.models.main_models import LopHoc


class ILopHocRepo(ABC):
    @abstractmethod
    async def check_existed(self, id: str) -> bool:
        pass

    @abstractmethod
    async def get_all(self) -> List[LopHoc]:
        pass

    @abstractmethod
    async def get_by_id(self, id: str) -> Optional[LopHoc]:
        pass

    @abstractmethod
    async def add(self, lop_hoc: LopHoc) -> LopHoc:
        pass

    @abstractmethod
    async def update(self, id: str, lop_hoc_data: Dict) -> Optional[LopHoc]:
        pass

    @abstractmethod
    async def delete(self, id: str) -> bool:
        pass 