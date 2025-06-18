from typing import Optional
from pydantic import BaseModel

class ClassResponse(BaseModel):
    id: Optional[str]
    name: str
    capacity: Optional[int] 