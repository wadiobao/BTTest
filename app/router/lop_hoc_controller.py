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
from app.models.lop_hoc_request import LopHocRequest
from app.services.lop_hoc_service import LopHocService
from app.database import create_db_and_tables, get_session, async_engine

async def get_lop_hoc_service(session: AsyncSession = Depends(get_session)) -> LopHocService:
    return LopHocService(session)

router = APIRouter(prefix="/lophoc")

@router.post("/lop/them/",response_model=CustomResponse)
async def them_lop(lopRequest: LopHocRequest, lop_hoc_service: LopHocService = Depends(get_lop_hoc_service)):
    data = await lop_hoc_service.them_lop_db(lopRequest)
    return CustomResponse(code=status.HTTP_200_OK,result=data)

@router.get("/lop/hienthi/tatca", response_model=CustomResponse)
async def hien_ds_lop(lop_hoc_service: LopHocService = Depends(get_lop_hoc_service)):
    data = await lop_hoc_service.hien_ds_lop_db()
    return CustomResponse(code=status.HTTP_200_OK,result=data)

@router.patch("/lop/sua/{id}",response_model=CustomResponse)
async def sua_lop(id: str =Path(...), lopHocRequest: LopHocRequest = Body(), lop_hoc_service: LopHocService = Depends(get_lop_hoc_service)):
    data = await lop_hoc_service.sua_lop_db(id,lopHocRequest)
    return CustomResponse(code=status.HTTP_200_OK,result=data)

@router.delete("/lophoc/xoa/",response_model=CustomResponse)
async def xoa_lop_theo_id(id: str = Query(...), lop_hoc_service: LopHocService  = Depends(get_lop_hoc_service)):
    data = await lop_hoc_service.xoa_lop_db(id)
    return CustomResponse(code=status.HTTP_200_OK,result=data)