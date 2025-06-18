from typing import Optional
from fastapi import APIRouter, Body, Depends, status, Query, Path
from sqlmodel.ext.asyncio.session import AsyncSession
from app.exceptions import ApiResponse
from app.services.student_service import StudentService
from app.database import get_session
from app.repository.student_repo import StudentRepo
from app.repository.faculty_repo import FacultyRepo
from app.models.request_models.student_request import StudentRequest

async def get_student_service(session: AsyncSession = Depends(get_session)) -> StudentService:
    return StudentService(StudentRepo(session), FacultyRepo(session))

router = APIRouter(prefix="/student")

@router.post("/create/", response_model=ApiResponse)
async def create_student(request: StudentRequest, student_service: StudentService = Depends(get_student_service)):
    data = await student_service.create_student(request)
    return ApiResponse(code=status.HTTP_200_OK, result=data)

@router.get("/all", response_model=ApiResponse)
async def get_all_students(student_service: StudentService = Depends(get_student_service)):
    data = await student_service.get_all_students()
    return ApiResponse(code=status.HTTP_200_OK, result=data)

@router.get("/by-age", response_model=ApiResponse)
async def get_students_by_age(order: Optional[str] = "desc", student_service: StudentService = Depends(get_student_service)):
    data = await student_service.get_students_by_age(order)
    return ApiResponse(code=status.HTTP_200_OK, result=data)

@router.get("/by-name", response_model=ApiResponse)
async def get_students_by_name(name: str = Query(...), student_service: StudentService = Depends(get_student_service)):
    data = await student_service.get_students_by_name(name)
    return ApiResponse(code=status.HTTP_200_OK, result=data)

@router.get("/by-id/{id}", response_model=ApiResponse)
async def get_student_by_id(id: int = Path(...), student_service: StudentService = Depends(get_student_service)):
    data = await student_service.get_student_by_id(id)
    return ApiResponse(code=status.HTTP_200_OK, result=data)

@router.patch("/update/{id}", response_model=ApiResponse)
async def update_student(id: int = Path(...), request: StudentRequest = Body(), student_service: StudentService = Depends(get_student_service)):
    data = await student_service.update_student(id, request)
    return ApiResponse(code=status.HTTP_200_OK, result=data)

@router.delete("/delete/", response_model=ApiResponse)
async def delete_student(id: int = Query(...), student_service: StudentService = Depends(get_student_service)):
    data = await student_service.delete_student(id)
    return ApiResponse(code=status.HTTP_200_OK, result=data) 
