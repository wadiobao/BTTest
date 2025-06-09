from typing import List, Optional
from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select, extract
from datetime import datetime

from app.database import get_session
from app.exceptions.CustomResponseException import CustomResponseException
from app.models.MainModels import Khoa, SinhVien
from app.models.SinhVienRequest import SinhVienRequest
from app.models.response_models import SinhVienResponse
from app.repository.IKhoaRepo import IKhoaRepo
from app.repository.ISinhVienRepo import ISinhVienRepo
from app.utils.mapper import map_sinhvien_to_response

class SinhVienService:
    def __init__(self, sv_repo: ISinhVienRepo, khoa_repo: IKhoaRepo):
        self.sv_repo = sv_repo
        self.khoa_repo = khoa_repo
    
    async def them_sinh_vien_db(self, sinhVienRequest: SinhVienRequest) -> Optional[SinhVienResponse]:
        khoa_existed = await self.khoa_repo.check_existed(sinhVienRequest.khoa_id)
        if not khoa_existed:
            raise CustomResponseException(
                message="Khoa không tồn tại")
            
        sinhVien = SinhVien.from_orm(sinhVienRequest)
        result = await self.sv_repo.add(sinhVien)
        return result
    
    async def hien_ds_sinh_vien_db(self) -> Optional[List[SinhVienResponse]]:
        sinhVienList = await self.sv_repo.display()
        sinhVienResponses = [map_sinhvien_to_response(sv) for sv in sinhVienList]
        return sinhVienResponses
    
    async def hien_ds_sinh_vien_tuoi_db(self, order: str) -> Optional[List[SinhVienResponse]]:
        sinhVienList
        if order == "giam":
            sinhVienList = self.sv_repo.display_by_age_desc()
        else:
            sinhVienList = self.sv_repo.display_by_age_asc()
            
        sinhVienResponses = [map_sinhvien_to_response(sv) for sv in sinhVienList]
        return sinhVienResponses
    
    async def hien_sinh_vien_id_db(self, id: int) -> Optional[SinhVienResponse]:
        sinhVien = self.sv_repo.display_by_id()
        if not sinhVien:
            raise CustomResponseException(
                message="Sinh viên không tồn tại")
        sinhVienResponse = map_sinhvien_to_response(sinhVien)
        return sinhVienResponse
    
    async def hien_sinh_vien_ten_db(self, ten: str) -> Optional[List[SinhVienResponse]]:    
        sinhVienList = self.sv_repo.display_by_name()
        if not sinhVienList:
            raise CustomResponseException(
                message="Sinh viên không tồn tại")
        
        sinhVienResponses = [map_sinhvien_to_response(sv) for sv in sinhVienList]
        return sinhVienResponses
    
    async def sua_sinh_vien_db(self, id: int, sinhVienRequest: SinhVienRequest) -> Optional[SinhVienResponse]:
        khoa_existed = await self.khoa_repo.check_existed(sinhVienRequest.khoa_id)
        if not khoa_existed:
            raise CustomResponseException(
                message="Khoa không tồn tại")
            
        sinhVien = await self.sv_repo.check_existed(id)
        if not sinhVien:
            raise CustomResponseException(
                message="Sinh viên không tồn tại")
            
        sinhVien_data = sinhVienRequest.model_dump(exclude_unset=True)
        sinhVien = self.sv_repo.update(id,sinhVien_data)
        sinhVienResponse = map_sinhvien_to_response(sinhVien)
        return sinhVienResponse
    
    async def xoa_sinh_vien_db(self, id: int) -> Optional[SinhVienResponse]:
        sv_existed = self.sv_repo.check_existed(id)
        if not sv_existed:
            raise CustomResponseException(
                message="Sinh viên không tồn tại")
        
        return self.sv_repo.delete(id)