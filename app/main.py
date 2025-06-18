import os
import re
from typing import Any, List, Optional, Set
from fastapi import Body, Depends, FastAPI, HTTPException, Header, Path, Request, status, Query #import class FastAPI() từ thư viện fastapi, 
import asyncio
from urllib.parse import quote_plus

from .exceptions.CustomResponseException import CustomResponse, CustomResponseException
from .exceptions.ExceptionHandler import exception_handler
from .router import gemini_controller,sinh_vien_controller,khoa_controller,lop_hoc_controller
from .database import create_db_and_tables, get_session, async_engine


app = FastAPI()

app.include_router(sinh_vien_controller.router)
app.include_router(khoa_controller.router)
app.include_router(lop_hoc_controller.router)
app.include_router(gemini_controller.router)


@app.on_event("startup")
async def start_up():
    await create_db_and_tables()

@app.on_event("shutdown")
async def shutdown():
    await async_engine.dispose()

exception_handler(app)

@app.get("/")
async def read_main():
    return {"msg": "Hello World"}