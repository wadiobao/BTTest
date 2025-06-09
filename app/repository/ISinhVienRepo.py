from abc import ABC, abstractmethod
from typing import Any, List

from annotated_types import T

class ISinhVienRepo(ABC):
    
    @abstractmethod
    async def check_existed(self,id:int) -> bool:
        pass
    
    @abstractmethod
    async def add(self, entity:T) -> int:
        pass
    
    @abstractmethod
    async def display(self) -> List[T]:
        pass
    
    @abstractmethod
    async def update(self,id:int,entity:T) -> int:
        pass
    
    @abstractmethod
    async def display_by_age_asc(self)-> List[T]:
        pass
    
    @abstractmethod
    async def display_by_age_desc(self)-> List[T]:
        pass
    
    @abstractmethod
    async def display_by_name(self,ten:str)-> List[T]:
        pass
    
    @abstractmethod
    async def display_by_id(self,id:int)-> T:
        pass
    
    @abstractmethod
    async def delete(self,id:int)-> int:
        pass