from typing import Optional
from sqlmodel import Field, SQLModel

from app.models.base_models.base_model import TimeStampedModel

class StudentClass(TimeStampedModel, table=True):
    """Association model for many-to-many relationship between Student and Class"""
    student_id: Optional[int] = Field(default=None, foreign_key="student.id", primary_key=True)
    class_id: Optional[str] = Field(default=None, foreign_key="classes.id", primary_key=True)
    
