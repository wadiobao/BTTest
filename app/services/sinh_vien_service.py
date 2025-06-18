from typing import List, Optional
from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import selectinload, joinedload
from sqlmodel import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy import extract
from datetime import datetime

from app.database import get_session
from app.exceptions import ResponseException
from app.models.base_models import Faculty, Student, Class
from app.models.response_models import SinhVienResponse
from app.utils.mapper import map_sinhvien_to_response
from app.models.request_models import StudentRequest
from app.repository.student_repo import StudentRepo
from app.repository.faculty_repo import FacultyRepo

class SinhVienService:
    def __init__(self, sv_repo: StudentRepo, khoa_repo: FacultyRepo):
        self.sv_repo = sv_repo
        self.khoa_repo = khoa_repo
    
    async def them_sinh_vien_db(self, sinhVienRequest: StudentRequest) -> Optional[SinhVienResponse]:
        khoa_existed = await self.khoa_repo.check_existed(sinhVienRequest.faculty_id)
        if not khoa_existed:
            raise ResponseException(
                message="Khoa không tồn tại")
            
        sinhVien = Student.from_orm(sinhVienRequest)
        result = await self.sv_repo.add(sinhVien)
        return result
    
    async def hien_ds_sinh_vien_db(self) -> Optional[List[SinhVienResponse]]:
        sinhVienList = await self.sv_repo.display()
        sinhVienResponses = [map_sinhvien_to_response(sv) for sv in sinhVienList]
        return sinhVienResponses
    
    async def hien_ds_sinh_vien_tuoi_db(self, order: str) -> Optional[List[SinhVienResponse]]:
        if order == "giam":
            sinhVienList = await self.sv_repo.display_by_age_desc()
        else:
            sinhVienList = await self.sv_repo.display_by_age_asc()
            
        sinhVienResponses = [map_sinhvien_to_response(sv) for sv in sinhVienList]
        return sinhVienResponses
    
    async def hien_sinh_vien_id_db(self, id: int) -> Optional[SinhVienResponse]:
        sinhVien = await self.sv_repo.display_by_id(id)
        if not sinhVien:
            raise ResponseException(
                message="Sinh viên không tồn tại")
        sinhVienResponse = map_sinhvien_to_response(sinhVien)
        return sinhVienResponse
    
    async def hien_sinh_vien_ten_db(self, ten: str) -> Optional[List[SinhVienResponse]]:    
        sinhVienList = await self.sv_repo.display_by_name(ten)
        if not sinhVienList:
            raise ResponseException(
                message="Sinh viên không tồn tại")
        
        sinhVienResponses = [map_sinhvien_to_response(sv) for sv in sinhVienList]
        return sinhVienResponses
    
    async def sua_sinh_vien_db(self, id: int, sinhVienRequest: StudentRequest) -> Optional[SinhVienResponse]:
        khoa_existed = await self.khoa_repo.check_existed(sinhVienRequest.faculty_id)
        if not khoa_existed:
            raise ResponseException(
                message="Khoa không tồn tại")
            
        sinhVien = await self.sv_repo.check_existed(id)
        if not sinhVien:
            raise ResponseException(
                message="Sinh viên không tồn tại")
            
        sinhVien_data = sinhVienRequest.model_dump(exclude_unset=True)
        await self.sv_repo.update(id, sinhVien_data)
        # Get the updated sinh vien object
        updated_sinh_vien = await self.sv_repo.display_by_id(id)
        sinhVienResponse = map_sinhvien_to_response(updated_sinh_vien)
        return sinhVienResponse
    
    async def xoa_sinh_vien_db(self, id: int) -> Optional[SinhVienResponse]:
        sv_existed = await self.sv_repo.check_existed(id)
        if not sv_existed:
            raise ResponseException(
                message="Sinh viên không tồn tại")
        
        return await self.sv_repo.delete(id)
