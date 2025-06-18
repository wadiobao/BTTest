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
import aiofiles
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
import threading

from app.exceptions import ApiResponse, ResponseException
from app.services.gemini_service import GeminiService
from app.services.faculty_service import KhoaService
from app.database import create_db_and_tables, get_session, async_engine
from app.repository.faculty_repo import KhoaRepo
from app.repository.gemini import GeminiRepo
from app.repository.gemini.document_store import DocumentStore

async def get_gemini_service(session: AsyncSession = Depends(get_session)) -> GeminiService:
    repo = GeminiRepo(session)
    return GeminiService(repo)
async def get_khoa_service(session: AsyncSession = Depends(get_session)) -> KhoaService:
    return KhoaService(KhoaRepo(session))

router = APIRouter(prefix="/chat")

# @router.post("/chat/database/")
# async def chat(request: ChatRequest, khoa_service: KhoaService = Depends(get_khoa_service)):
#     data = await khoa_service.hien_ds_khoa_db()
#     response = GeminiService.get_response_with_context_from_database(request,str(data))
#     return CustomResponse(code=status.HTTP_200_OK,result=response)

# @router.post("/chat/")
# async def chat_database(request: ChatRequest):
#     response = GeminiService.get_response(request)
#     return CustomResponse(code=status.HTTP_200_OK,result=response)

@router.post("/demo-rag/")
async def demo_rag(
    prompt: str = Form(...), 
    
    gemini_service: GeminiService = Depends(get_gemini_service)
):
    response = await gemini_service.rag_demo(prompt=prompt)
    return CustomResponse(code=status.HTTP_200_OK, result=response)

@router.post("/add/")
async def add_file(
    file: UploadFile = File(...),
    gemini_service: GeminiService = Depends(get_gemini_service)
):
    response = await gemini_service.add_file(file=file)
    return CustomResponse(code=status.HTTP_200_OK, result=response)


@router.post("/summary/")
async def rag_tom_tat(
    prompt: str = Form(...), 
    gemini_service: GeminiService = Depends(get_gemini_service)
):
    response = await gemini_service.rag_tom_tat(prompt=prompt)
    return CustomResponse(code=status.HTTP_200_OK, result=response)
