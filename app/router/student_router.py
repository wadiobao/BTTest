from typing import Optional
from fastapi import APIRouter, Body, Depends, status, Query, Path
from sqlmodel.ext.asyncio.session import AsyncSession
from app.exceptions import ApiResponse, ResponseException
from app.services.student_service import StudentService
from app.database import get_session
from app.repository.student_repo.student_repo import StudentRepo
from app.repository.faculty_repo.faculty_repo import FacultyRepo
from app.models.request_models.student_request import StudentRequest

async def get_student_service(session: AsyncSession = Depends(get_session)) -> StudentService:
    return StudentService(StudentRepo(session), FacultyRepo(session))

router = APIRouter(prefix="/student")

@router.post("/create/", response_model=ApiResponse)
async def create_student(request: StudentRequest, student_service: StudentService = Depends(get_student_service)):
    try:
        data = await student_service.create_student(request)
        return ApiResponse(code=status.HTTP_200_OK, result=data)
    except ResponseException as e:
        if "does not exist" in str(e):
            return ApiResponse(code=status.HTTP_404_NOT_FOUND, status="error", result=f"Create student failed: {str(e)}")
        return ApiResponse(code=status.HTTP_422_UNPROCESSABLE_ENTITY, status="error", result=f"Create student failed: {str(e)}")
    except Exception as e:
        return ApiResponse(code=status.HTTP_500_INTERNAL_SERVER_ERROR, status="error", result="Internal server error, please contact admin.")

@router.get("/all", response_model=ApiResponse)
async def get_all_students(student_service: StudentService = Depends(get_student_service)):
    try:
        data = await student_service.get_all_students()
        return ApiResponse(code=status.HTTP_200_OK, result=data)
    except Exception as e:
        return ApiResponse(code=status.HTTP_500_INTERNAL_SERVER_ERROR, status="error", result="Internal server error")

@router.get("/by-age", response_model=ApiResponse)
async def get_students_by_age(order: Optional[str] = "desc", student_service: StudentService = Depends(get_student_service)):
    try:
        data = await student_service.get_students_by_age(order)
        return ApiResponse(code=status.HTTP_200_OK, result=data)
    except Exception as e:
        return ApiResponse(code=status.HTTP_500_INTERNAL_SERVER_ERROR, status="error", result="Internal server error")

@router.get("/by-name", response_model=ApiResponse)
async def get_students_by_name(name: str = Query(...), student_service: StudentService = Depends(get_student_service)):
    try:
        data = await student_service.get_students_by_name(name)
        return ApiResponse(code=status.HTTP_200_OK, result=data)
    except ResponseException as e:
        if "does not exist" in str(e):
            return ApiResponse(code=status.HTTP_404_NOT_FOUND, status="error", result=f"Student not found: {str(e)}")
        return ApiResponse(code=status.HTTP_422_UNPROCESSABLE_ENTITY, status="error", result=f"Student error: {str(e)}")
    except Exception as e:
        return ApiResponse(code=status.HTTP_500_INTERNAL_SERVER_ERROR, status="error", result="Internal server error, please contact admin.")

@router.get("/by-id/{id}", response_model=ApiResponse)
async def get_student_by_id(id: int = Path(...), student_service: StudentService = Depends(get_student_service)):
    try:
        data = await student_service.get_student_by_id(id)
        return ApiResponse(code=status.HTTP_200_OK, result=data)
    except ResponseException as e:
        if "does not exist" in str(e):
            return ApiResponse(code=status.HTTP_404_NOT_FOUND, status="error", result=f"Student not found: {str(e)}")
        return ApiResponse(code=status.HTTP_422_UNPROCESSABLE_ENTITY, status="error", result=f"Student error: {str(e)}")
    except Exception as e:
        return ApiResponse(code=status.HTTP_500_INTERNAL_SERVER_ERROR, status="error", result="Internal server error, please contact admin.")

@router.patch("/update/{id}", response_model=ApiResponse)
async def update_student(id: int = Path(...), request: StudentRequest = Body(), student_service: StudentService = Depends(get_student_service)):
    try:
        data = await student_service.update_student(id, request)
        return ApiResponse(code=status.HTTP_200_OK, result=data)
    except ResponseException as e:
        if "does not exist" in str(e):
            return ApiResponse(code=status.HTTP_404_NOT_FOUND, status="error", result=f"Update student failed: {str(e)}")
        return ApiResponse(code=status.HTTP_422_UNPROCESSABLE_ENTITY, status="error", result=f"Update student failed: {str(e)}")
    except Exception as e:
        return ApiResponse(code=status.HTTP_500_INTERNAL_SERVER_ERROR, status="error", result="Internal server error, please contact admin.")

@router.delete("/delete/", response_model=ApiResponse)
async def delete_student(id: int = Query(...), student_service: StudentService = Depends(get_student_service)):
    try:
        data = await student_service.delete_student(id)
        return ApiResponse(code=status.HTTP_200_OK, result=data)
    except ResponseException as e:
        if "does not exist" in str(e):
            return ApiResponse(code=status.HTTP_404_NOT_FOUND, status="error", result=f"Delete student failed: {str(e)}")
        return ApiResponse(code=status.HTTP_422_UNPROCESSABLE_ENTITY, status="error", result=f"Delete student failed: {str(e)}")
    except Exception as e:
        return ApiResponse(code=status.HTTP_500_INTERNAL_SERVER_ERROR, status="error", result="Internal server error, please contact admin.") 
