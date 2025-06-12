from abc import ABC, abstractmethod
from typing import Any, List

from annotated_types import T

class IKhoaRepo(ABC):
    
    @abstractmethod
    async def check_existed(self,id:int) -> bool:
        pass
    

