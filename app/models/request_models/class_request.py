from typing import Optional, List
from sqlmodel import SQLModel

class ClassRequest(SQLModel):
    """Request model for class operations"""
    id: Optional[str] = None
    name: Optional[str] = None
    capacity: Optional[int] = None
    student_ids: Optional[List[int]] = []
    
    class Config:
        orm_mode = True 
