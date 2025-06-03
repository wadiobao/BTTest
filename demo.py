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

class Khoa(SQLModel,table = True):
    id : Optional[str] = Field(default=None,primary_key=True)
    ten_khoa: str = Field(index=True)
    ds_sinh_vien: List["SinhVien"] = Relationship(back_populates="khoa",sa_relationship_kwargs={"lazy": "selectin"})

class KhoaRequest(SQLModel):
    id : Optional[str] = None
    ten_khoa: Optional[str] = None
    class Config:
        orm_mode: True

class KhoaResponse(SQLModel):
    id : str
    ten_khoa: str
    ds_sinh_vien: Optional[List["SinhVien"]]
    
class SinhVienLopHoc(SQLModel, table=True):
    sinh_vien_id: Optional[int] = Field(default=None, foreign_key="sinhvien.id", primary_key=True)
    lop_hoc_id: Optional[str] = Field(default=None, foreign_key="lophoc.id", primary_key=True)

class SinhVien(SQLModel, table = True):
    id: Optional[int] = Field(default=None,primary_key=True)
    ten_sinh_vien: str = Field(index=True)
    gioi_tinh: str
    ngay_sinh:  date
    sdt : str
    email: str
    que_quan: str
    khoa : Optional[Khoa] = Relationship(back_populates="ds_sinh_vien",sa_relationship_kwargs={"lazy": "selectin"})
    khoa_id : Optional[str] = Field(default=None, foreign_key="khoa.id",nullable=True)
    ds_lop_hoc: Optional[List["LopHoc"]] = Relationship(back_populates="ds_sinh_vien",sa_relationship_kwargs={"lazy": "selectin"},link_model=SinhVienLopHoc)

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


class LopHoc(SQLModel, table=True):
    id : Optional[str] = Field(default=None,primary_key=True)
    ten_lop_hoc: str = Field(index=True)
    si_so: int = Field(default=None)
    ds_sinh_vien: Optional[List[SinhVien]] = Relationship(back_populates="ds_lop_hoc",sa_relationship_kwargs={"lazy": "selectin"},link_model=SinhVienLopHoc)
    
class LopHocRequest(SQLModel):
    id : Optional[str] = None
    ten_lop_hoc: Optional[str] = None
    si_so: Optional[int]
    ds_sinh_vien: Optional[List[int]] = []
    class Config:
        orm_mode: True
        
class LopHocResponse(SQLModel):
    id : str
    ten_lop_hoc: str
    si_so: int
    ds_sinh_vien: Optional[List[SinhVien]]
    
    
def map_sinhvien_to_response(sinhVien: SinhVien) -> SinhVienResponse:
    return SinhVienResponse(
        id=sinhVien.id,
        ten_sinh_vien=sinhVien.ten_sinh_vien,
        gioi_tinh=sinhVien.gioi_tinh,
        ngay_sinh=sinhVien.ngay_sinh,
        sdt=sinhVien.sdt,
        email=sinhVien.email,
        que_quan=sinhVien.que_quan,
        khoa=sinhVien.khoa.ten_khoa if sinhVien.khoa else None,
        ds_lop_hoc=sinhVien.ds_lop_hoc
    )

def map_khoa_to_response(khoa: Khoa) -> KhoaResponse:
    return KhoaResponse(
        id=khoa.id,
        ten_khoa=khoa.ten_khoa,
        ds_sinh_vien=[
            map_sinhvien_to_response(sv) for sv in khoa.ds_sinh_vien
        ]
    )
    
def map_lop_to_response(lop: LopHoc) -> LopHocResponse:
    return LopHocResponse(
        id=lop.id,
        ten_lop_hoc=lop.ten_lop_hoc,
        si_so=lop.si_so,
        ds_sinh_vien=lop.ds_sinh_vien
    )
    
class CustomResponse(BaseModel):
    code: int
    status: str = Field(default="success")
    result: Any
    
class CustomResponseException(Exception):
    message:str
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)
    

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

async def them_sinh_vien_db(sinhVienRequest: SinhVienRequest)-> Optional[SinhVienResponse]:
    async with AsyncSession(async_engine) as session:
        khoa = await session.get(Khoa, sinhVienRequest.khoa_id)
        if not khoa:
            raise CustomResponseException(
                message="Khoa không tồn tại")
        sinhVien = SinhVien.from_orm(sinhVienRequest)
        session.add(sinhVien)
        await session.commit()
        await session.refresh(sinhVien)
        sinhVienResponse = map_sinhvien_to_response(sinhVien)
        return sinhVienResponse
    
async def them_khoa_db(khoaRequest: KhoaRequest)-> Optional[KhoaResponse]:
    async with AsyncSession(async_engine) as session:
        khoa = await session.get(Khoa, khoaRequest.id)
        if khoa:
            raise CustomResponseException(
                message="Khoa đã tồn tại")
        khoa = Khoa.from_orm(khoaRequest)
        session.add(khoa)
        await session.commit()
        await session.refresh(khoa)
        khoaResponse = map_khoa_to_response(khoa)
        return khoaResponse
    
async def them_lop_db(lopHocRequest: LopHocRequest)-> Optional[LopHocResponse]:
    async with AsyncSession(async_engine) as session:
        lopHoc = await session.get(LopHoc, lopHocRequest.id)
        if lopHoc:
            raise CustomResponseException(
                message="Lớp học đã tồn tại")
        lopHoc = LopHoc.from_orm(lopHocRequest)
        session.add(lopHoc)
        await session.commit()
        await session.refresh(lopHoc)
        lopHocResponse = map_lop_to_response(lopHoc)
        return lopHocResponse
    

async def hien_ds_sinh_vien_db() -> Optional[List[SinhVienResponse]]:
    async with AsyncSession(async_engine) as session:
        result = await session.execute(
            select(SinhVien)
            .options(
                selectinload(SinhVien.khoa),
                selectinload(SinhVien.ds_lop_hoc)
            )
        )
        sinhVienList = result.scalars().all()
        sinhVienResponses = [map_sinhvien_to_response(sv) for sv in sinhVienList]
        return sinhVienResponses
    
async def hien_ds_sinh_vien_tuoi_db(order:str) -> Optional[List[SinhVienResponse]]:
    async with AsyncSession(async_engine) as session:
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
            
        result = await session.execute(stmt)
        sinhVienList = result.scalars().all()
        sinhVienResponses = [map_sinhvien_to_response(sv) for sv in sinhVienList]
        return sinhVienResponses
    
async def hien_sinh_vien_id_db(id: int) -> Optional[SinhVienResponse]:
    async with AsyncSession(async_engine) as session:
        stmt = (
            select(SinhVien)
            .options(
                selectinload(SinhVien.khoa),
                selectinload(SinhVien.ds_lop_hoc)
            )
        ).where(SinhVien.id==id)
        result = await session.execute(stmt)
        sinhVien = result.scalar_one_or_none()
        if not sinhVien:
            raise CustomResponseException(
                message="Sinh viên không  tồn tại")
        sinhVienResponse = map_sinhvien_to_response(sinhVien)
        return sinhVienResponse
    
async def hien_sinh_vien_ten_db(ten: str) -> Optional[List[SinhVienResponse]]:
    async with AsyncSession(async_engine) as session:
        stmt = (
            select(SinhVien)
            .options(
                selectinload(SinhVien.khoa),
                selectinload(SinhVien.ds_lop_hoc)
            )
        ).where(SinhVien.ten_sinh_vien.like(f"%{ten}%"))   
        result = await session.execute(stmt)    
        sinhVienList = result.scalars().all()
        if not sinhVienList:
            raise CustomResponseException(
                message="Sinh viên không  tồn tại")
        
        sinhVienResponses = [map_sinhvien_to_response(sv) for sv in sinhVienList]
        return sinhVienResponses
    
async def hien_ds_khoa_db() -> Optional[List[KhoaResponse]]:
    async with AsyncSession(async_engine) as session:
        result = await session.execute(
            select(Khoa)
            .options(
                selectinload(Khoa.ds_sinh_vien)
            )
        )
        khoaList = result.scalars().all()
        khoaResponses = [map_khoa_to_response(k) for k in khoaList]
        return khoaResponses
    
async def hien_khoa_ten_db(ten: str) -> Optional[List[KhoaResponse]]:
    async with AsyncSession(async_engine) as session:
        stmt = (
            select(Khoa)
            .options(
                selectinload(Khoa.ds_sinh_vien)
            )
        ).where(Khoa.ten_khoa.like(f"%{ten}%"))   
        result = await session.execute(stmt)    

        khoaList = result.scalars().all()
        if not khoaList:
            raise CustomResponseException(
                message="Khoa không  tồn tại")
        
        khoaResponses = [map_khoa_to_response(k) for k in khoaList]
        return khoaResponses

async def hien_ds_lop_db() -> Optional[List[LopHocResponse]]:
    async with AsyncSession(async_engine) as session:
        stmt = (
            select(LopHoc) 
            .options(
                selectinload(LopHoc.ds_sinh_vien).selectinload(SinhVien.khoa)
            )
        )
        result = await session.execute(stmt)
        lopHocList = result.scalars().all()
        lopHocResponses = [map_lop_to_response(lh) for lh in lopHocList]
        return lopHocResponses
    
async def sua_sinh_vien_db(id: int,sinhVienRequest: SinhVienRequest) -> Optional[SinhVienResponse]:
    async with AsyncSession(async_engine) as session:
        khoa = await session.get(Khoa, sinhVienRequest.khoa_id)
        if not khoa:
            raise CustomResponseException(
                message="Khoa không tồn tại")
        sinhVien = await session.get(SinhVien,id)
        if not sinhVien:
            raise CustomResponseException(
                message="Sinh viên không  tồn tại")
        sinhVien_data = sinhVienRequest.model_dump(exclude_unset=True)
        sinhVien.sqlmodel_update(sinhVien_data)
        session.add(sinhVien)
        await session.commit()
        await session.refresh(sinhVien) 
        sinhVienResponse = map_sinhvien_to_response(sinhVien)
        return sinhVienResponse
    
async def sua_khoa_db(id: str, khoaRequest: KhoaRequest)-> Optional[KhoaResponse]:
    async with AsyncSession(async_engine) as session:
        khoa = await session.get(Khoa, id)
        if not khoa:
            raise CustomResponseException(
                message="Khoa không tồn tại")
        khoa.ten_khoa = khoaRequest.ten_khoa
        session.add(khoa)
        await session.commit()
        await session.refresh(khoa)
        khoaResponse = map_khoa_to_response(khoa)
        return khoaResponse

async def sua_lop_db(id: str, lopHocRequest: LopHocRequest)-> Optional[LopHocResponse]:
    async with AsyncSession(async_engine) as session:
        result = await session.execute(
            select(LopHoc)
            .options(selectinload(LopHoc.ds_sinh_vien))
            .where(LopHoc.id == id)
        )
        lopHoc = result.scalar_one_or_none()
        if not lopHoc:
            raise CustomResponseException(
                message="Lớp không tồn tại")
        lopHoc.ten_lop_hoc = lopHocRequest.ten_lop_hoc
        new_sinh_vien_objects = []
        for svid in lopHocRequest.ds_sinh_vien:
            sinhVien = await session.get(SinhVien,svid)
            if not sinhVien:
                raise CustomResponseException(
                message="có sinh viên không  tồn tại")
            new_sinh_vien_objects.append(sinhVien)
        lopHoc.ds_sinh_vien = new_sinh_vien_objects
        session.add(lopHoc)
        await session.commit()
        await session.refresh(lopHoc)
        lopResponse = map_lop_to_response(lopHoc)
        return lopResponse
    
async def xoa_sinh_vien_db(id:int)-> Optional[SinhVienResponse]:
    async with AsyncSession(async_engine) as session:
        stmt = (
            select(SinhVien)
            .options(
                selectinload(SinhVien.khoa),
                selectinload(SinhVien.ds_lop_hoc)
            )
        ).where(SinhVien.id==id)
        result = await session.execute(stmt)
        sinhVien = result.scalar_one_or_none()
        if not sinhVien:
            raise CustomResponseException(
                message="Sinh viên không  tồn tại")
        sinhVienResponse = map_sinhvien_to_response(sinhVien)
        sinhVien.ds_lop_hoc = []
        sinhVien.khoa = None
        await session.delete(sinhVien)
        await session.commit()
        return sinhVienResponse
    
async def xoa_khoa_db(id:str)-> Optional[KhoaResponse]:
    async with AsyncSession(async_engine) as session:
        stmt = (
            select(Khoa)
            .options(
                selectinload(Khoa.ds_sinh_vien)
            )
        ).where(Khoa.id==id)   
        result = await session.execute(stmt)    
        khoa = result.scalar_one_or_none()
        
        if not khoa:
            raise CustomResponseException(
                message="Khoa không tồn tại")
        
        khoaResponse = map_khoa_to_response(khoa)
        dsSinhVien = [map_sinhvien_to_response(sv) for sv in khoa.ds_sinh_vien]
        khoaResponse.ds_sinh_vien = dsSinhVien

        for sv in khoa.ds_sinh_vien:
            sv.khoa_id = None
            sv.khoa = None
        
        await session.delete(khoa)
        await session.commit()
        
        return khoaResponse
    
async def xoa_lop_db(id:str)-> Optional[LopHocResponse]:
    async with AsyncSession(async_engine) as session:
        stmt = (
            select(LopHoc)
            .options(
                selectinload(LopHoc.ds_sinh_vien).selectinload(SinhVien.khoa)
            )
        ).where(LopHoc.id==id)   
        result = await session.execute(stmt)    
        lopHoc = result.scalar_one_or_none()
        
        if not lopHoc:
            raise CustomResponseException(
                message="Lớp không tồn tại")
        
        lopHocResponse = map_lop_to_response(lopHoc)
        
        if lopHoc.ds_sinh_vien:
            lopHoc.ds_sinh_vien.clear()
        
        await session.delete(lopHoc)
        await session.commit()
        
        return lopHocResponse
    
app = FastAPI()

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