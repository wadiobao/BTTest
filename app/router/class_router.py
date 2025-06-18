from typing import Optional
from fastapi import APIRouter, Body, Depends, status, Query, Path
from sqlmodel.ext.asyncio.session import AsyncSession
from app.exceptions import ApiResponse
from app.services.class_service import ClassService
from app.database import get_session
from app.repository.class_repo import ClassRepo
from app.models.request_models.class_request import ClassRequest

async def get_class_service(session: AsyncSession = Depends(get_session)) -> ClassService:
    return ClassService(ClassRepo(session))

router = APIRouter(prefix="/class")

@router.post("/create/", response_model=ApiResponse)
async def create_class(request: ClassRequest, class_service: ClassService = Depends(get_class_service)):
    data = await class_service.them_lop_hoc_db(request)
    return ApiResponse(code=status.HTTP_200_OK, result=data)

@router.get("/all", response_model=ApiResponse)
async def get_all_classes(class_service: ClassService = Depends(get_class_service)):
    data = await class_service.hien_ds_lop_hoc_db()
    return ApiResponse(code=status.HTTP_200_OK, result=data)

@router.patch("/update/{id}", response_model=ApiResponse)
async def update_class(id: str = Path(...), request: ClassRequest = Body(), class_service: ClassService = Depends(get_class_service)):
    data = await class_service.cap_nhat_lop_hoc_db(id, request)
    return ApiResponse(code=status.HTTP_200_OK, result=data)

@router.delete("/delete/", response_model=ApiResponse)
async def delete_class(id: str = Query(...), class_service: ClassService = Depends(get_class_service)):
    data = await class_service.xoa_lop_hoc_db(id)
    return ApiResponse(code=status.HTTP_200_OK, result=data) 
