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
from app.models.KhoaRequest import KhoaRequest
from app.models.LopHocRequest import LopHocRequest
from app.models.SinhVienRequest import SinhVienRequest
from app.services import SinhVienService
from app.services.KhoaService import KhoaService
from app.services.LopHocService import LopHocService

DB_USER = os.getenv("MYSQL_USER", "root")
DB_PASS = os.getenv("MYSQL_PASSWORD", "default_password")
DB_HOST = os.getenv("MYSQL_HOST", "db")  # Changed from localhost to db for Docker
DB_PORT = os.getenv("MYSQL_PORT", "3306")
DB_NAME = os.getenv("MYSQL_DATABASE", "quan_li_sinh_vien")

# Build the database URL
DATABASE_URL = f"mysql+aiomysql://{DB_USER}:{quote_plus(DB_PASS)}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

async_engine = create_async_engine(DATABASE_URL, echo=True)

async def create_db_and_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

async def get_session():
    async with AsyncSession(async_engine) as session:
        yield session

app = FastAPI()


async def get_khoa_service(session: AsyncSession = Depends(get_session)) -> KhoaService:
    return KhoaService(session)

async def get_sinh_vien_service(session: AsyncSession = Depends(get_session)) -> SinhVienService:
    return SinhVienService(session)

async def get_lop_hoc_service(session: AsyncSession = Depends(get_session)) -> LopHocService:
    return LopHocService(session)

@app.on_event("startup")
async def start_up():
    await create_db_and_tables()

@app.post("/sinhvien/them/", response_model=CustomResponse)
async def them_sinh_vien(sinhVienRequest: SinhVienRequest):
    data = await them_sinh_vien_db(sinhVienRequest)
    return CustomResponse(code=status.HTTP_200_OK,result=data)

@app.post("/khoa/them/",response_model=CustomResponse)
async def them_khoa(khoaRequest: KhoaRequest):
    data = await them_khoa_db(khoaRequest)
    return CustomResponse(code=status.HTTP_200_OK,result=data)

@app.post("/lop/them/",response_model=CustomResponse)
async def them_lop(lopRequest: LopHocRequest):
    data=await them_lop_db(lopRequest)
    return CustomResponse(code=status.HTTP_200_OK,result=data)
####################################################################################
@app.get("/sinhvien/hienthi/tatca", response_model=CustomResponse)
async def hien_ds_sinh_vien():
    data = await hien_ds_sinh_vien_db()
    return CustomResponse(code=status.HTTP_200_OK,result=data)

@app.get("/sinhvien/hienthi/tuoi", response_model=CustomResponse)
async def hien_ds_sinh_vien_tuoi_giam_dan(order:Optional[str]="giam"):
    data= await hien_ds_sinh_vien_tuoi_db(order)
    return CustomResponse(code=status.HTTP_200_OK,result=data)

@app.get("/sinhvien/hienthi/ten", response_model=CustomResponse)
async def hien_sinh_vien_theo_ten(ten:str=Query(...)):
    data= await hien_sinh_vien_ten_db(ten)
    return CustomResponse(code=status.HTTP_200_OK,result=data)

@app.get("/sinhvien/hienthi/{id}", response_model=CustomResponse)
async def hien_sinh_vien_theo_id(id: int =Path(...)):
    data= await hien_sinh_vien_id_db(id)
    return CustomResponse(code=status.HTTP_200_OK,result=data)

@app.get("/khoa/hienthi/tatca", response_model=CustomResponse)
async def hien_ds_khoa():
    data= await hien_ds_khoa_db()
    return CustomResponse(code=status.HTTP_200_OK,result=data)

@app.get("/khoa/hienthi/ten", response_model=CustomResponse)
async def hien_khoa_theo_ten(ten:str=Query(...)):
    data= await hien_khoa_ten_db(ten)
    return CustomResponse(code=status.HTTP_200_OK,result=data)

@app.get("/lop/hienthi/tatca", response_model=CustomResponse)
async def hien_ds_lop():
    data= await hien_ds_lop_db()
    return CustomResponse(code=status.HTTP_200_OK,result=data)
#######################################################################################
@app.patch("/sinhvien/sua/{id}",response_model=CustomResponse)
async def sua_sinh_vien(id: int =Path(...), sinhVienRequest: SinhVienRequest = Body()):
    data= await sua_sinh_vien_db(id,sinhVienRequest)
    return CustomResponse(code=status.HTTP_200_OK,result=data)

@app.patch("/khoa/sua/{id}",response_model=CustomResponse)
async def sua_khoa(id: str =Path(...), khoaRequest: KhoaRequest = Body()):
    data = await sua_khoa_db(id,khoaRequest)
    return CustomResponse(code=status.HTTP_200_OK,result=data)

@app.patch("/lop/sua/{id}",response_model=CustomResponse)
async def sua_lop(id: str =Path(...), lopHocRequest: LopHocRequest = Body()):
    data= await sua_lop_db(id,lopHocRequest)
    return CustomResponse(code=status.HTTP_200_OK,result=data)
#######################################################################################

@app.delete("/sinhvien/xoa/",response_model=CustomResponse)
async def xoa_sinh_vien_theo_id(id: int = Query(...)):
    data= await xoa_sinh_vien_db(id)
    return CustomResponse(code=status.HTTP_200_OK,result=data)

@app.delete("/khoa/xoa/",response_model=CustomResponse)
async def xoa_khoa_theo_id(id: str = Query(...)):
    data= await xoa_khoa_db(id)
    return CustomResponse(code=status.HTTP_200_OK,result=data)

@app.delete("/lophoc/xoa/",response_model=CustomResponse)
async def xoa_lop_theo_id(id: str = Query(...)):
    data= await xoa_lop_db(id)
    return CustomResponse(code=status.HTTP_200_OK,result=data)




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
    custom_error_response= CustomResponse(
        code= status.HTTP_422_UNPROCESSABLE_ENTITY,
        status= "error",
        result= exc.message
    )
    
    return JSONResponse(
        status_code= status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=custom_error_response
    )
    
@app.exception_handler(TypeError)
async def validation_value_error(request: Request, exc: TypeError):
    custom_error_response= CustomResponse(
        code= status.HTTP_422_UNPROCESSABLE_ENTITY,
        status= "error",
        result= exc.message
    )
    
    return JSONResponse(
        status_code= status.HTTP_417_EXPECTATION_FAILED,
        content=custom_error_response
    )

@app.exception_handler(AttributeError)
async def validation_value_error(request: Request, exc: AttributeError):
    custom_error_response= CustomResponse(
        code= status.HTTP_422_UNPROCESSABLE_ENTITY,
        status= "error",
        result= exc.message
    )
    
    return JSONResponse(
        status_code= status.HTTP_417_EXPECTATION_FAILED,
        content=custom_error_response
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
    
@app.exception_handler(AttributeError)
async def validation_value_error(request: Request, exc: AttributeError):
    custom_error_response= CustomResponse(
        code= status.HTTP_422_UNPROCESSABLE_ENTITY,
        status= "error",
        result= exc.message
    )
    
    return JSONResponse(
        status_code= status.HTTP_417_EXPECTATION_FAILED,
        content=custom_error_response.model_dump()
    )