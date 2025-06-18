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

class SinhVienRequest(SQLModel):
    ten_sinh_vien: Optional[str] = None
    gioi_tinh: Optional[str] = None
    ngay_sinh:  Optional[date]
    sdt : Optional[str] = None
    email: str
    que_quan: Optional[str] = None
    khoa_id : Optional[str] = None
    class Config:
        orm_mode: True
    
    @field_validator("gioi_tinh")
    def validate_gioi_tinh(cls,v):
        if v.lower() not in ("nam", "nữ", "nu"):
            raise CustomResponseException(
                message="Giới tính phải là 'Nam' hoặc 'Nữ'"
            )
        return v.title()
    
    @field_validator("sdt")
    def validate_sdt(cls,v):
        if not re.match(r"^(0|\+84)[0-9]{9}$", v):
            raise CustomResponseException(
                message="Số điện thoại không hợp lệ")
        return v
    
    @field_validator("ngay_sinh",mode="after")
    @classmethod
    def validate_ngay_sinh(cls,v:Optional[date]):
        today = date.today()
        birth_date = v
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        if age <= 18:
            raise CustomResponseException(
                message="Sinh viên phải đủ 18 tuổi trở lên.")
        return v
    
    @field_validator('email')
    @classmethod
    def validate_email_format(cls, v: str) -> str:
        email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.fullmatch(email_regex, v):
            raise CustomResponseException(
                message="Email không hợp lệ. Vui lòng nhập email đúng định dạng.")
        return v