import os
import re
from typing import Any, List, Optional, Set
from fastapi import Body, Depends, FastAPI, HTTPException, Header, Path, Request, status, Query #import class FastAPI() từ thư viện fastapi, 
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr, Field, HttpUrl, field_validator, validator
from sqlalchemy import URL
from sqlmodel import Field, Relationship, SQLModel, extract, select 
from sqlalchemy.ext.asyncio import create_async_engine
from datetime import date, datetime, timedelta
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
import asyncio
from urllib.parse import quote_plus

from app.exceptions.CustomResponseException import CustomResponseException
from app.models.MainModels import Khoa,SinhVien,LopHoc
from app.models.SinhVienRequest import SinhVienRequest
from app.models.SinhVienResponse import SinhVienResponse
from app.utils.mapper import map_sinhvien_to_response

class SinhVien:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def them_sinh_vien_db(self,sinhVienRequest: SinhVienRequest)-> Optional[SinhVienResponse]:
        khoa = await self.session.get(Khoa, sinhVienRequest.khoa_id)
        if not khoa:
            raise CustomResponseException(
                message="Khoa không tồn tại")
        sinhVien = SinhVien.from_orm(sinhVienRequest)
        self.session.add(sinhVien)
        await self.session.commit()
        await self.session.refresh(sinhVien)
        sinhVienResponse = map_sinhvien_to_response(sinhVien)
        return sinhVienResponse
    
    async def hien_ds_sinh_vien_db(self) -> Optional[List[SinhVienResponse]]:
        result = await self.session.execute(
            select(SinhVien)
            .options(
                selectinload(SinhVien.khoa),
                selectinload(SinhVien.ds_lop_hoc)
            )
        )
        sinhVienList = result.scalars().all()
        sinhVienResponses = [map_sinhvien_to_response(sv) for sv in sinhVienList]
        return sinhVienResponses
    
    async def hien_ds_sinh_vien_tuoi_db(self,order:str) -> Optional[List[SinhVienResponse]]:
        current_year = datetime.now().year
        stmt = (
            select(SinhVien)
            .options(
                selectinload(SinhVien.khoa),
                selectinload(SinhVien.ds_lop_hoc)
            )
        )
        
        if order == "giam":
            stmt = stmt.order_by((extract('year', SinhVien.ngay_sinh)-current_year).desc())
        else:
            stmt = stmt.order_by((extract('year', SinhVien.ngay_sinh)-current_year).asc())
            
        result = await self.session.execute(stmt)
        sinhVienList = result.scalars().all()
        sinhVienResponses = [map_sinhvien_to_response(sv) for sv in sinhVienList]
        return sinhVienResponses
    
    async def hien_sinh_vien_id_db(self,id: int) -> Optional[SinhVienResponse]:
        stmt = (
            select(SinhVien)
            .options(
                selectinload(SinhVien.khoa),
                selectinload(SinhVien.ds_lop_hoc)
            )
        ).where(SinhVien.id==id)
        result = await self.session.execute(stmt)
        sinhVien = result.scalar_one_or_none()
        if not sinhVien:
            raise CustomResponseException(
                message="Sinh viên không  tồn tại")
        sinhVienResponse = map_sinhvien_to_response(sinhVien)
        return sinhVienResponse
    
    async def hien_sinh_vien_ten_db(self,ten: str) -> Optional[List[SinhVienResponse]]:
        stmt = (
            select(SinhVien)
            .options(
                selectinload(SinhVien.khoa),
                selectinload(SinhVien.ds_lop_hoc)
            )
        ).where(SinhVien.ten_sinh_vien.like(f"%{ten}%"))   
        result = await self.session.execute(stmt)    
        sinhVienList = result.scalars().all()
        if not sinhVienList:
            raise CustomResponseException(
                message="Sinh viên không  tồn tại")
        
        sinhVienResponses = [map_sinhvien_to_response(sv) for sv in sinhVienList]
        return sinhVienResponses
    
    async def sua_sinh_vien_db(self,id: int,sinhVienRequest: SinhVienRequest) -> Optional[SinhVienResponse]:
        khoa = await self.session.get(Khoa, sinhVienRequest.khoa_id)
        if not khoa:
            raise CustomResponseException(
                message="Khoa không tồn tại")
        sinhVien = await self.session.get(SinhVien,id)
        if not sinhVien:
            raise CustomResponseException(
                message="Sinh viên không  tồn tại")
        sinhVien_data = sinhVienRequest.model_dump(exclude_unset=True)
        sinhVien.sqlmodel_update(sinhVien_data)
        self.session.add(sinhVien)
        await self.session.commit()
        await self.session.refresh(sinhVien) 
        sinhVienResponse = map_sinhvien_to_response(sinhVien)
        return sinhVienResponse
    
    async def xoa_sinh_vien_db(self,id:int)-> Optional[SinhVienResponse]:
        stmt = (
            select(SinhVien)
            .options(
                selectinload(SinhVien.khoa),
                selectinload(SinhVien.ds_lop_hoc)
            )
        ).where(SinhVien.id==id)
        result = await self.session.execute(stmt)
        sinhVien = result.scalar_one_or_none()
        if not sinhVien:
            raise CustomResponseException(
                message="Sinh viên không  tồn tại")
        sinhVienResponse = map_sinhvien_to_response(sinhVien)
        sinhVien.ds_lop_hoc = []
        sinhVien.khoa = None
        await self.session.delete(sinhVien)
        await self.session.commit()
        return sinhVienResponse