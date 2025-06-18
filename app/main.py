import os
import re
from typing import Any, List, Optional, Set
from fastapi import Body, Depends, FastAPI, HTTPException, Header, Path, Request, status, Query #import class FastAPI() từ thư viện fastapi, 
import asyncio
from urllib.parse import quote_plus
from fastapi.middleware.cors import CORSMiddleware

from .exceptions import ApiResponse, ResponseException, setup_exception_handlers
from .router import faculty_router, student_router, class_router, gemini_router
from .database import create_db_and_tables, get_session, async_engine


app = FastAPI(title="API Documentation", version="1.0.0")

app.include_router(student_router.router)
app.include_router(faculty_router.router)
app.include_router(class_router.router)
app.include_router(gemini_router.router)

# Setup exception handlers
setup_exception_handlers(app)

@app.on_event("startup")
async def start_up():
    await create_db_and_tables()

@app.on_event("shutdown")
async def shutdown():
    await async_engine.dispose()

@app.get("/")
async def read_main():
    return {"msg": "Hello World"}