from typing import Optional
from sqlmodel import SQLModel

class FacultyRequest(SQLModel):
    """Request model for faculty operations"""
    id: Optional[str] = None
    name: Optional[str] = None
    
    class Config:
        orm_mode = True 
