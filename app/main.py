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
from app.models.ChatRequest import ChatRequest
from app.models.KhoaRequest import KhoaRequest
from app.models.LopHocRequest import LopHocRequest
from app.models.SinhVienRequest import SinhVienRequest
from app.services.GeminiService import GeminiService
from app.services.SinhVienService import SinhVienService
from app.services.KhoaService import KhoaService
from app.services.LopHocService import LopHocService
from app.database import create_db_and_tables, get_session

app = FastAPI()

async def get_khoa_service(session: AsyncSession = Depends(get_session)) -> KhoaService:
    return KhoaService(session)

async def get_sinh_vien_service(session: AsyncSession = Depends(get_session)) -> SinhVienService:
    return SinhVienService(session)

async def get_lop_hoc_service(session: AsyncSession = Depends(get_session)) -> LopHocService:
    return LopHocService(session)

async def get_gemini_service(session: AsyncSession = Depends(get_session)) -> GeminiService:
    return GeminiService(session)

@app.on_event("startup")
async def start_up():
    await create_db_and_tables()

@app.on_event("shutdown")
async def shutdown():
    await async_engine.dispose()

@app.post("/sinhvien/them/", response_model=CustomResponse)
async def them_sinh_vien(sinhVienRequest: SinhVienRequest, sinh_vien_service: SinhVienService = Depends(get_sinh_vien_service)):
    data = await sinh_vien_service.them_sinh_vien_db(sinhVienRequest)
    return CustomResponse(code=status.HTTP_200_OK, result=data)

@app.post("/khoa/them/",response_model=CustomResponse)
async def them_khoa(khoaRequest: KhoaRequest, khoa_service: KhoaService = Depends(get_khoa_service)):
    data = await khoa_service.them_khoa_db(khoaRequest)
    return CustomResponse(code=status.HTTP_200_OK,result=data)

@app.post("/lop/them/",response_model=CustomResponse)
async def them_lop(lopRequest: LopHocRequest, lop_hoc_service: LopHocService = Depends(get_lop_hoc_service)):
    data = await lop_hoc_service.them_lop_db(lopRequest)
    return CustomResponse(code=status.HTTP_200_OK,result=data)
####################################################################################
@app.get("/sinhvien/hienthi/tatca", response_model=CustomResponse)
async def hien_ds_sinh_vien(sinh_vien_service: SinhVienService = Depends(get_sinh_vien_service)):
    data = await sinh_vien_service.hien_ds_sinh_vien_db()
    return CustomResponse(code=status.HTTP_200_OK, result=data)

@app.get("/sinhvien/hienthi/tuoi", response_model=CustomResponse)
async def hien_ds_sinh_vien_tuoi_giam_dan(order: Optional[str] = "giam", sinh_vien_service: SinhVienService = Depends(get_sinh_vien_service)):
    data = await sinh_vien_service.hien_ds_sinh_vien_tuoi_db(order)
    return CustomResponse(code=status.HTTP_200_OK, result=data)

@app.get("/sinhvien/hienthi/ten", response_model=CustomResponse)
async def hien_sinh_vien_theo_ten(ten: str = Query(...), sinh_vien_service: SinhVienService = Depends(get_sinh_vien_service)):
    data = await sinh_vien_service.hien_sinh_vien_ten_db(ten)
    return CustomResponse(code=status.HTTP_200_OK, result=data)

@app.get("/sinhvien/hienthi/{id}", response_model=CustomResponse)
async def hien_sinh_vien_theo_id(id: int = Path(...), sinh_vien_service: SinhVienService = Depends(get_sinh_vien_service)):
    data = await sinh_vien_service.hien_sinh_vien_id_db(id)
    return CustomResponse(code=status.HTTP_200_OK, result=data)

@app.get("/khoa/hienthi/tatca", response_model=CustomResponse)
async def hien_ds_khoa(khoa_service: KhoaService = Depends(get_khoa_service)):
    data = await khoa_service.hien_ds_khoa_db()
    return CustomResponse(code=status.HTTP_200_OK,result=data)

@app.get("/khoa/hienthi/ten", response_model=CustomResponse)
async def hien_khoa_theo_ten(ten:str=Query(...), khoa_service: KhoaService = Depends(get_khoa_service)):
    data = await khoa_service.hien_khoa_ten_db(ten)
    return CustomResponse(code=status.HTTP_200_OK,result=data)

@app.get("/lop/hienthi/tatca", response_model=CustomResponse)
async def hien_ds_lop(lop_hoc_service: LopHocService = Depends(get_lop_hoc_service)):
    data = await lop_hoc_service.hien_ds_lop_db()
    return CustomResponse(code=status.HTTP_200_OK,result=data)
#######################################################################################
@app.patch("/sinhvien/sua/{id}",response_model=CustomResponse)
async def sua_sinh_vien(id: int = Path(...), sinhVienRequest: SinhVienRequest = Body(), sinh_vien_service: SinhVienService = Depends(get_sinh_vien_service)):
    data = await sinh_vien_service.sua_sinh_vien_db(id, sinhVienRequest)
    return CustomResponse(code=status.HTTP_200_OK,result=data)

@app.patch("/khoa/sua/{id}",response_model=CustomResponse)
async def sua_khoa(id: str =Path(...), khoaRequest: KhoaRequest = Body(), khoa_service: KhoaService = Depends(get_khoa_service)):
    data = await khoa_service.sua_khoa_db(id,khoaRequest)
    return CustomResponse(code=status.HTTP_200_OK,result=data)

@app.patch("/lop/sua/{id}",response_model=CustomResponse)
async def sua_lop(id: str =Path(...), lopHocRequest: LopHocRequest = Body(), lop_hoc_service: LopHocService = Depends(get_lop_hoc_service)):
    data = await lop_hoc_service.sua_lop_db(id,lopHocRequest)
    return CustomResponse(code=status.HTTP_200_OK,result=data)
#######################################################################################

@app.delete("/sinhvien/xoa/",response_model=CustomResponse)
async def xoa_sinh_vien_theo_id(id: int = Query(...), sinh_vien_service: SinhVienService = Depends(get_sinh_vien_service)):
    data= await sinh_vien_service.xoa_sinh_vien_db(id)
    return CustomResponse(code=status.HTTP_200_OK,result=data)

@app.delete("/khoa/xoa/",response_model=CustomResponse)
async def xoa_khoa_theo_id(id: str = Query(...), khoa_service: KhoaService = Depends(get_khoa_service)):
    data = await khoa_service.xoa_khoa_db(id)
    return CustomResponse(code=status.HTTP_200_OK,result=data)

@app.delete("/lophoc/xoa/",response_model=CustomResponse)
async def xoa_lop_theo_id(id: str = Query(...), lop_hoc_service: LopHocService  = Depends(get_lop_hoc_service)):
    data = await lop_hoc_service.xoa_lop_db(id)
    return CustomResponse(code=status.HTTP_200_OK,result=data)

#######################################################################################
@app.post("/chat/")
async def chat(request: ChatRequest, khoa_service: KhoaService = Depends(get_khoa_service)):
    data = await khoa_service.hien_ds_khoa_db()
    response = GeminiService.get_response(request,str(data))
    return CustomResponse(code=status.HTTP_200_OK,result=response)

@app.post("/chat/database/")
async def chat_database(request: ChatRequest, gemini_service: GeminiService = Depends(get_gemini_service)):
    response = await gemini_service.get_response_with_context_from_database(request)
    return CustomResponse(code=status.HTTP_200_OK,result=response)


@app.exception_handler(RequestValidationError)
async def custom_validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Custom exception handler để định dạng lại lỗi xác thực Pydantic.
    Cố gắng lấy thông báo lỗi cụ thể từ lỗi đầu tiên.
    """

    # Mặc định là một thông báo chung
    error_message_to_display = "Dữ liệu đầu vào không hợp lệ. Vui lòng kiểm tra các trường đã gửi."

    # Cố gắng lấy thông báo lỗi cụ thể từ lỗi đầu tiên nếu có
    if exc.errors():
        first_error = exc.errors()[0]
        # Lấy msg từ lỗi đầu tiên.
        # Hoặc có thể lấy thông báo lỗi từ ctx['error'] nếu đó là ValueError từ custom validator
        if 'msg' in first_error:
            # Pydantic v2 thường có 'msg' chứa thông báo lỗi tổng quát (e.g., "Value error, Giới tính phải là 'Nam' hoặc 'Nữ'")
            # và 'ctx' chứa đối tượng lỗi gốc.
            # Bạn có thể chọn cái nào phù hợp hơn.
            # Ở đây, tôi sẽ ưu tiên thông báo từ ctx['error'] nếu nó là ValueError gốc.
            if 'ctx' in first_error and 'error' in first_error['ctx'] and isinstance(first_error['ctx']['error'], ValueError):
                error_message_to_display = str(first_error['ctx']['error'])
            else:
                error_message_to_display = first_error['msg']
        elif 'type' in first_error:
            error_message_to_display = f"Lỗi xác thực kiểu dữ liệu: {first_error['type']}"

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "status": "error",
            "code": status.HTTP_422_UNPROCESSABLE_ENTITY,
            "message": error_message_to_display, # Sử dụng thông báo lỗi cụ thể
            # "timestamp": datetime.now().isoformat() # Tùy chọn
        },
    )
    
@app.exception_handler(ValueError)
async def validation_value_error(request: Request, exc: ValueError):
    custom_error_response = CustomResponse(
        code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        status="error",
        result=str(exc)
    )
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=custom_error_response.model_dump()
    )
    
@app.exception_handler(TypeError)
async def validation_type_error(request: Request, exc: TypeError):
    custom_error_response = CustomResponse(
        code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        status="error",
        result=str(exc)
    )
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=custom_error_response.model_dump()
    )

@app.exception_handler(AttributeError)
async def validation_value_error(request: Request, exc: AttributeError):
    custom_error_response = CustomResponse(
        code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        status="error",
        result=str(exc)
    )
    
    return JSONResponse(
        status_code=status.HTTP_417_EXPECTATION_FAILED,
        content=custom_error_response.model_dump()
    )

@app.exception_handler(CustomResponseException)
async def validation_value_error(request: Request, exc: CustomResponseException):
    custom_error_response= CustomResponse(
        code= status.HTTP_422_UNPROCESSABLE_ENTITY,
        status= "error",
        result= exc.message
    )
    
    return JSONResponse(
        status_code= status.HTTP_417_EXPECTATION_FAILED,
        content=custom_error_response.model_dump()
    )