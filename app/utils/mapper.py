from app.models.base_models import Faculty, Student, Classes
from app.models.response_models import FacultyResponse, StudentResponse, ClassResponse
from datetime import datetime

def map_lop_to_response(lopHoc: Classes) -> ClassResponse:
    return ClassResponse(
        id=lopHoc.id,
        name=lopHoc.name,
        capacity=lopHoc.capacity
    )

def map_sinhvien_to_response(sinhVien: Student) -> StudentResponse:
    return StudentResponse(
        id=sinhVien.id,
        name=sinhVien.name,
        gender=sinhVien.gender,
        birth_date=sinhVien.birth_date.date() if isinstance(sinhVien.birth_date, datetime) else sinhVien.birth_date,
        phone=sinhVien.phone,
        email=sinhVien.email,
        hometown=sinhVien.hometown,
        faculty=sinhVien.faculty.name if sinhVien.faculty else None,
        classes=[map_lop_to_response(lh) for lh in sinhVien.classes] if hasattr(sinhVien, 'classes') and sinhVien.classes else None
    )

def map_khoa_to_response(khoa: Faculty) -> FacultyResponse:
    return FacultyResponse(
        id=khoa.id,
        name=khoa.name,
        students=[map_sinhvien_to_response(sv) for sv in khoa.students] if hasattr(khoa, 'students') and khoa.students else None
    )

def map_lop_hoc_to_response(lop_hoc: Classes) -> ClassResponse:
    return ClassResponse(
        id=lop_hoc.id,
        name=lop_hoc.name,
        capacity=lop_hoc.capacity
    )

def map_sinh_vien_to_response(sinh_vien: Student) -> StudentResponse:
    return StudentResponse(
        id=sinh_vien.id,
        name=sinh_vien.name,
        gender=sinh_vien.gender,
        birth_date=sinh_vien.birth_date,
        phone=sinh_vien.phone,
        email=sinh_vien.email,
        hometown=sinh_vien.hometown,
        faculty=sinh_vien.faculty.name if sinh_vien.faculty else None
    )
    