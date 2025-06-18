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
from app.models.khoa_request import KhoaRequest
from app.services.khoa_service import KhoaService
from app.database import create_db_and_tables, get_session, async_engine
from app.repository.khoa_repo import KhoaRepo

async def get_khoa_service(session: AsyncSession = Depends(get_session)) -> KhoaService:
    return KhoaService(KhoaRepo(session))

router = APIRouter(prefix="/khoa")

@router.post("/them/",response_model=CustomResponse)
async def them_khoa(khoaRequest: KhoaRequest, khoa_service: KhoaService = Depends(get_khoa_service)):
    data = await khoa_service.them_khoa_db(khoaRequest)
    return CustomResponse(code=status.HTTP_200_OK,result=data)

@router.get("/hienthi/tatca", response_model=CustomResponse)
async def hien_ds_khoa(khoa_service: KhoaService = Depends(get_khoa_service)):
    data = await khoa_service.hien_ds_khoa_db()
    return CustomResponse(code=status.HTTP_200_OK,result=data)

@router.get("/hienthi/ten", response_model=CustomResponse)
async def hien_khoa_theo_ten(ten:str=Query(...), khoa_service: KhoaService = Depends(get_khoa_service)):
    data = await khoa_service.hien_khoa_ten_db(ten)
    return CustomResponse(code=status.HTTP_200_OK,result=data)

@router.patch("/sua/{id}",response_model=CustomResponse)
async def sua_khoa(id: str =Path(...), khoaRequest: KhoaRequest = Body(), khoa_service: KhoaService = Depends(get_khoa_service)):
    data = await khoa_service.cap_nhat_khoa_db(id,khoaRequest)
    return CustomResponse(code=status.HTTP_200_OK,result=data)

@router.delete("/xoa/",response_model=CustomResponse)
async def xoa_khoa_theo_id(id: str = Query(...), khoa_service: KhoaService = Depends(get_khoa_service)):
    data = await khoa_service.xoa_khoa_db(id)
    return CustomResponse(code=status.HTTP_200_OK,result=data)

@router.get("/hienthi/{id}", response_model=CustomResponse)
async def hien_khoa_theo_id(id: str = Path(...), khoa_service: KhoaService = Depends(get_khoa_service)):
    data = await khoa_service.hien_khoa_theo_id_db(id)
    return CustomResponse(code=status.HTTP_200_OK,result=data)