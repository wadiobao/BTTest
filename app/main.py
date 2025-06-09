import os
import re
from typing import Any, List, Optional, Set
from fastapi import Body, Depends, FastAPI, HTTPException, Header, Path, Request, status, Query #import class FastAPI() từ thư viện fastapi, 
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
from app.exceptions.ExceptionHandler import exception_handler
from app.models.ChatRequest import ChatRequest
from app.models.KhoaRequest import KhoaRequest
from app.models.LopHocRequest import LopHocRequest
from app.models.SinhVienRequest import SinhVienRequest
from app.router import GeminiController, KhoaController, LopHocController, SinhVienController
from app.services.GeminiService import GeminiService
from app.services.SinhVienService import SinhVienService
from app.services.KhoaService import KhoaService
from app.services.LopHocService import LopHocService
from app.database import create_db_and_tables, get_session, async_engine
from app.repository.SinhVienRepo import SinhVienRepo
from app.repository.KhoaRepo import KhoaRepo

app = FastAPI()

app.include_router(SinhVienController.router)
app.include_router(KhoaController.router)
app.include_router(LopHocController.router)
app.include_router(GeminiController.router)


@app.on_event("startup")
async def start_up():
    await create_db_and_tables()

@app.on_event("shutdown")
async def shutdown():
    await async_engine.dispose()

exception_handler(app)

