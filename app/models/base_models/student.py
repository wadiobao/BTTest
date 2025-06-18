from typing import List, Optional
from datetime import date
from sqlmodel import Field, Relationship, SQLModel

from app.models.base_models.base_model import TimeStampedModel
from .student_class import StudentClass

class Student(TimeStampedModel, table=True):
    """Student model representing a student in the university"""
    id: Optional[int] = Field(default=None, primary_key=True, description="Student ID")
    name: str = Field(index=True, description="Student name")
    gender: str = Field(description="Student gender (Nam/Nữ)")
    birth_date: date = Field(description="Student birth date")
    phone: str = Field(description="Student phone number")
    email: str = Field(description="Student email")
    hometown: str = Field(description="Student hometown")
    
    # Foreign keys
    faculty_id: Optional[str] = Field(default=None, foreign_key="faculty.id", nullable=True, description="Faculty ID")
    
    # Relationships
    faculty: Optional["Faculty"] = Relationship(back_populates="students")
    classes: List["Classes"] = Relationship(back_populates="students", link_model=StudentClass)
