import os
import re
from typing import Any, List, Optional, Set
from fastapi import APIRouter, Body, Depends, FastAPI, File, HTTPException, Header, Path, Request, UploadFile, status, Query, Form #import class FastAPI() từ thư viện fastapi, 
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
from app.models.ChatRequest import ChatRequest
from app.models.KhoaRequest import KhoaRequest
from app.models.LopHocRequest import LopHocRequest
from app.models.SinhVienRequest import SinhVienRequest
from app.services.GeminiService import GeminiService
from app.services.SinhVienService import SinhVienService
from app.services.KhoaService import KhoaService
from app.services.LopHocService import LopHocService
from app.database import create_db_and_tables, get_session, async_engine
from app.repository.SinhVienRepo import SinhVienRepo
from app.repository.KhoaRepo import KhoaRepo

async def get_gemini_service(session: AsyncSession = Depends(get_session)) -> GeminiService:
    return GeminiService(session)
async def get_khoa_service(session: AsyncSession = Depends(get_session)) -> KhoaService:
    return KhoaService(KhoaRepo(session))

router = APIRouter(prefix="/chat")

@router.post("/chat/database/")
async def chat(request: ChatRequest, khoa_service: KhoaService = Depends(get_khoa_service)):
    data = await khoa_service.hien_ds_khoa_db()
    response = GeminiService.get_response_with_context_from_database(request,str(data))
    return CustomResponse(code=status.HTTP_200_OK,result=response)

@router.post("/chat/")
async def chat_database(request: ChatRequest):
    response = GeminiService.get_response(request)
    return CustomResponse(code=status.HTTP_200_OK,result=response)

@router.post("/demo-rag/")
async def demo_rag(prompt: str = Form(...), file: UploadFile = File(...)):
    response = await GeminiService.rag_demo(prompt, file)
    return CustomResponse(code=status.HTTP_200_OK, result=response)
 