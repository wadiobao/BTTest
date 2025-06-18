from typing import List, Optional
from pydantic import BaseModel
from .student_response import StudentResponse
 
class FacultyResponse(BaseModel):
    id: str
    name: str
    students: Optional[List[StudentResponse]] = None 