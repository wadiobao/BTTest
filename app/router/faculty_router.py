from typing import Optional
from fastapi import APIRouter, Body, Depends, status, Query, Path
from sqlmodel.ext.asyncio.session import AsyncSession
from app.exceptions import ApiResponse, ResponseException
from app.services.faculty_service import FacultyService
from app.database import get_session
from app.repository.faculty_repo.faculty_repo import FacultyRepo
from app.models.request_models.faculty_request import FacultyRequest

async def get_faculty_service(session: AsyncSession = Depends(get_session)) -> FacultyService:
    return FacultyService(FacultyRepo(session))

router = APIRouter(prefix="/faculty")

@router.post("/create/", response_model=ApiResponse)
async def create_faculty(request: FacultyRequest, faculty_service: FacultyService = Depends(get_faculty_service)):
    try:
        data = await faculty_service.create_faculty(request)
        return ApiResponse(code=status.HTTP_200_OK, result=data)
    except ResponseException as e:
        return ApiResponse(code=status.HTTP_422_UNPROCESSABLE_ENTITY, status="error", result=f"Create faculty failed: {str(e)}")
    except Exception as e:
        return ApiResponse(code=status.HTTP_500_INTERNAL_SERVER_ERROR, status="error", result="Internal server error, please contact admin.")

@router.get("/all", response_model=ApiResponse)
async def get_all_faculties(faculty_service: FacultyService = Depends(get_faculty_service)):
    try:
        data = await faculty_service.get_all_faculties()
        return ApiResponse(code=status.HTTP_200_OK, result=data)
    except ResponseException as e:
        return ApiResponse(code=status.HTTP_422_UNPROCESSABLE_ENTITY, status="error", result=str(e))
    except Exception as e:
        return ApiResponse(code=status.HTTP_500_INTERNAL_SERVER_ERROR, status="error", result="Internal server error")

@router.get("/by-name", response_model=ApiResponse)
async def get_faculty_by_name(name: str = Query(...), faculty_service: FacultyService = Depends(get_faculty_service)):
    try:
        data = await faculty_service.get_faculty_by_name(name)
        return ApiResponse(code=status.HTTP_200_OK, result=data)
    except ResponseException as e:
        return ApiResponse(code=status.HTTP_422_UNPROCESSABLE_ENTITY, status="error", result=str(e))
    except Exception as e:
        return ApiResponse(code=status.HTTP_500_INTERNAL_SERVER_ERROR, status="error", result="Internal server error")

@router.patch("/update/{id}", response_model=ApiResponse)
async def update_faculty(id: str = Path(...), request: FacultyRequest = Body(), faculty_service: FacultyService = Depends(get_faculty_service)):
    try:
        data = await faculty_service.update_faculty(id, request)
        return ApiResponse(code=status.HTTP_200_OK, result=data)
    except ResponseException as e:
        return ApiResponse(code=status.HTTP_422_UNPROCESSABLE_ENTITY, status="error", result=str(e))
    except Exception as e:
        return ApiResponse(code=status.HTTP_500_INTERNAL_SERVER_ERROR, status="error", result="Internal server error")

@router.delete("/delete/", response_model=ApiResponse)
async def delete_faculty(id: str = Query(...), faculty_service: FacultyService = Depends(get_faculty_service)):
    try:
        data = await faculty_service.delete_faculty(id)
        return ApiResponse(code=status.HTTP_200_OK, result=data)
    except ResponseException as e:
        return ApiResponse(code=status.HTTP_422_UNPROCESSABLE_ENTITY, status="error", result=str(e))
    except Exception as e:
        return ApiResponse(code=status.HTTP_500_INTERNAL_SERVER_ERROR, status="error", result="Internal server error")

@router.get("/by-id/{id}", response_model=ApiResponse)
async def get_faculty_by_id(id: str = Path(...), faculty_service: FacultyService = Depends(get_faculty_service)):
    try:
        data = await faculty_service.get_faculty_by_id(id)
        return ApiResponse(code=status.HTTP_200_OK, result=data)
    except ResponseException as e:
        return ApiResponse(code=status.HTTP_404_NOT_FOUND, status="error", result=f"Faculty not found: {str(e)}")
    except Exception as e:
        return ApiResponse(code=status.HTTP_500_INTERNAL_SERVER_ERROR, status="error", result="Internal server error, please contact admin.") 
