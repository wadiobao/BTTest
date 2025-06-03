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

class SinhVienResponse(SQLModel):
    id: Optional[int] = None
    ten_sinh_vien: str
    gioi_tinh: str
    ngay_sinh:  date
    sdt : str
    email: str
    que_quan: str
    khoa: Optional[str]
    ds_lop_hoc: Optional[List["LopHoc"]]