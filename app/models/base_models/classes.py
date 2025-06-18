from typing import List, Optional
from sqlmodel import Field, Relationship
from app.models.base_models.base_model import TimeStampedModel
from .student_class import StudentClass


class Classes(TimeStampedModel, table=True):
    id: Optional[str] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    capacity: int = Field(default=None)
    
    # Relationships
    students: List["Student"] = Relationship(back_populates="classes", link_model=StudentClass)
