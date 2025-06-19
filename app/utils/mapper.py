from app.models.base_models import Faculty, Student, Classes
from app.models.response_models import FacultyResponse, StudentResponse, ClassResponse
from datetime import datetime

def mapClassToResponse(class_obj: Classes) -> ClassResponse:
    return ClassResponse(
        id=class_obj.id,
        name=class_obj.name,
        capacity=class_obj.capacity
    )

def mapStudentToResponse(student: Student) -> StudentResponse:
    return StudentResponse(
        id=student.id,
        name=student.name,
        gender=student.gender,
        birth_date=student.birth_date.date() if isinstance(student.birth_date, datetime) else student.birth_date,
        phone=student.phone,
        email=student.email,
        hometown=student.hometown,
        faculty=student.faculty.name if student.faculty else None,
        classes=[mapClassToResponse(cls) for cls in student.classes] if hasattr(student, 'classes') and student.classes else None
    )

def mapFacultyToResponse(faculty: Faculty) -> FacultyResponse:
    return FacultyResponse(
        id=faculty.id,
        name=faculty.name,
        students=[mapStudentToResponse(st) for st in faculty.students] if hasattr(faculty, 'students') and faculty.students else None
    )

