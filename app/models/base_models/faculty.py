from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel

from app.models.base_models.base_model import TimeStampedModel

class Faculty(TimeStampedModel, table=True):
    """Faculty model representing a faculty in the university"""
    id: Optional[str] = Field(default=None, primary_key=True, description="Faculty ID")
    name: str = Field(index=True, description="Faculty name")
    
    # Relationships
    students: List["Student"] = Relationship(back_populates="faculty")
    
