from typing import List, Optional
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select

from app.exceptions.CustomResponseException import CustomResponseException
from app.models.LopHocRequest import LopHocRequest
from app.models.LopHocResponse import LopHocResponse
from app.models.MainModels import LopHoc, SinhVien
from app.utils.mapper import map_lop_to_response

class LopHocService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def them_lop_db(self,lopHocRequest: LopHocRequest)-> Optional[LopHocResponse]:
    
        lopHoc = await self.session.get(LopHoc, lopHocRequest.id)
        if lopHoc:
            raise CustomResponseException(
                message="Lớp học đã tồn tại")
        lopHoc = LopHoc.from_orm(lopHocRequest)
        self.session.add(lopHoc)
        await self.session.commit()
        await self.session.refresh(lopHoc)
        lopHocResponse = map_lop_to_response(lopHoc)
        return lopHocResponse
    
    async def hien_ds_lop_db(self) -> Optional[List[LopHocResponse]]:
        stmt = (
            select(LopHoc) 
            .options(
                selectinload(LopHoc.ds_sinh_vien).selectinload(SinhVien.khoa)
            )
        )
        result = await self.session.execute(stmt)
        lopHocList = result.scalars().all()
        lopHocResponses = [map_lop_to_response(lh) for lh in lopHocList]
        return lopHocResponses

    async def sua_lop_db(self,id: str, lopHocRequest: LopHocRequest)-> Optional[LopHocResponse]:
        result = await self.session.execute(
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
            sinhVien = await self.session.get(SinhVien,svid)
            if not sinhVien:
                raise CustomResponseException(
                message="có sinh viên không  tồn tại")
            new_sinh_vien_objects.append(sinhVien)
        lopHoc.ds_sinh_vien = new_sinh_vien_objects
        self.session.add(lopHoc)
        await self.session.commit()
        await self.session.refresh(lopHoc)
        lopResponse = map_lop_to_response(lopHoc)
        return lopResponse
    
    async def xoa_lop_db(self,id:str)-> Optional[LopHocResponse]:
        stmt = (
            select(LopHoc)
            .options(
                selectinload(LopHoc.ds_sinh_vien).selectinload(SinhVien.khoa)
            )
        ).where(LopHoc.id==id)   
        result = await self.session.execute(stmt)    
        lopHoc = result.scalar_one_or_none()
        
        if not lopHoc:
            raise CustomResponseException(
                message="Lớp không tồn tại")
        
        lopHocResponse = map_lop_to_response(lopHoc)
        
        if lopHoc.ds_sinh_vien:
            lopHoc.ds_sinh_vien.clear()
        
        await self.session.delete(lopHoc)
        await self.session.commit()
        
        return lopHocResponse