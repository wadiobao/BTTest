from typing import List, Optional
from datetime import date
from pydantic import BaseModel
from .class_response import ClassResponse

class StudentResponse(BaseModel):
    id: Optional[int] = None
    name: str
    gender: str
    birth_date: date
    phone: str
    email: str
    hometown: str
    faculty: Optional[str]
    classes: Optional[List[ClassResponse]] = None 
