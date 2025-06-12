import os
import re
from typing import Any, List, Optional, Set
from fastapi import APIRouter, Body, Depends, FastAPI, HTTPException, Header, Path, Request, status, Query #import class FastAPI() từ thư viện fastapi, 
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlmodel import Field, Relationship, SQLModel, extract, select 
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
import asyncio
from urllib.parse import quote_plus

from app.exceptions.CustomResponseException import CustomResponse, CustomResponseException
from app.models.sinh_vien_request import SinhVienRequest
from app.services.sinh_vien_service import SinhVienService
from app.database import create_db_and_tables, get_session, async_engine
from app.repository.sinh_vien_repo import SinhVienRepo
from app.repository.khoa_repo import KhoaRepo

async def get_sinh_vien_service(session: AsyncSession = Depends(get_session)) -> SinhVienService:
    return SinhVienService(SinhVienRepo(session), KhoaRepo(session))

router = APIRouter(prefix="/sinhvien")

@router.post("/them/", response_model=CustomResponse)
async def them_sinh_vien123(sinhVienRequest: SinhVienRequest, sinh_vien_service: SinhVienService = Depends(get_sinh_vien_service)):
    data = await sinh_vien_service.them_sinh_vien_db(sinhVienRequest)
    return CustomResponse(code=status.HTTP_200_OK, result=data)

@router.get("/hienthi/tatca", response_model=CustomResponse)
async def hien_ds_sinh_vien123(sinh_vien_service: SinhVienService = Depends(get_sinh_vien_service)):
    data = await sinh_vien_service.hien_ds_sinh_vien_db()
    return CustomResponse(code=status.HTTP_200_OK, result=data)

@router.get("/sinhvien/hienthi/tuoi", response_model=CustomResponse)
async def hien_ds_sinh_vien_tuoi_giam_dan(order: Optional[str] = "giam", sinh_vien_service: SinhVienService = Depends(get_sinh_vien_service)):
    data = await sinh_vien_service.hien_ds_sinh_vien_tuoi_db(order)
    return CustomResponse(code=status.HTTP_200_OK, result=data)

@router.get("/sinhvien/hienthi/ten", response_model=CustomResponse)
async def hien_sinh_vien_theo_ten(ten: str = Query(...), sinh_vien_service: SinhVienService = Depends(get_sinh_vien_service)):
    data = await sinh_vien_service.hien_sinh_vien_ten_db(ten)
    return CustomResponse(code=status.HTTP_200_OK, result=data)

@router.get("/sinhvien/hienthi/{id}", response_model=CustomResponse)
async def hien_sinh_vien_theo_id(id: int = Path(...), sinh_vien_service: SinhVienService = Depends(get_sinh_vien_service)):
    data = await sinh_vien_service.hien_sinh_vien_id_db(id)
    return CustomResponse(code=status.HTTP_200_OK, result=data)

@router.patch("/sinhvien/sua/{id}",response_model=CustomResponse)
async def sua_sinh_vien(id: int = Path(...), sinhVienRequest: SinhVienRequest = Body(), sinh_vien_service: SinhVienService = Depends(get_sinh_vien_service)):
    data = await sinh_vien_service.sua_sinh_vien_db(id, sinhVienRequest)
    return CustomResponse(code=status.HTTP_200_OK,result=data)

@router.delete("/sinhvien/xoa/",response_model=CustomResponse)
async def xoa_sinh_vien_theo_id(id: int = Query(...), sinh_vien_service: SinhVienService = Depends(get_sinh_vien_service)):
    data= await sinh_vien_service.xoa_sinh_vien_db(id)
    return CustomResponse(code=status.HTTP_200_OK,result=data)