# app/services/khoa.py
from typing import List, Optional
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select

from app.exceptions.CustomResponseException import CustomResponseException
from app.models.MainModels import Khoa, SinhVien 
from app.models.KhoaRequest import KhoaRequest 
from app.models.KhoaResponse import KhoaResponse
from app.utils.mapper import map_khoa_to_response, map_sinhvien_to_response 


class KhoaService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def them_khoa_db(self ,khoaRequest: KhoaRequest)-> Optional[KhoaResponse]:
        khoa = await self.session.get(Khoa, khoaRequest.id)
        if khoa:
            raise CustomResponseException(
                message="Khoa đã tồn tại")
        khoa = Khoa.from_orm(khoaRequest)
        self.session.add(khoa)
        await self.session.commit()
        await self.session.refresh(khoa)
        khoaResponse = map_khoa_to_response(khoa)
        return khoaResponse

    async def hien_ds_khoa_db(self) -> Optional[List[KhoaResponse]]:
        result = await self.session.execute(
            select(Khoa)
            .options(
                selectinload(Khoa.ds_sinh_vien)
            )
        )
        khoaList = result.scalars().all()
        khoaResponses = [map_khoa_to_response(k) for k in khoaList]
        return khoaResponses

    async def hien_khoa_ten_db(self,ten: str) -> Optional[List[KhoaResponse]]:
        stmt = (
            select(Khoa)
            .options(
                selectinload(Khoa.ds_sinh_vien)
            )
        ).where(Khoa.ten_khoa.like(f"%{ten}%"))   
        result = await self.session.execute(stmt)    

        khoaList = result.scalars().all()
        if not khoaList:
            raise CustomResponseException(
                message="Khoa không  tồn tại")
        
        khoaResponses = [map_khoa_to_response(k) for k in khoaList]
        return khoaResponses

    async def sua_khoa_db(self,id: str, khoaRequest: KhoaRequest)-> Optional[KhoaResponse]:
        khoa = await self.session.get(Khoa, id)
        if not khoa:
            raise CustomResponseException(
                message="Khoa không tồn tại")
        khoa.ten_khoa = khoaRequest.ten_khoa
        self.session.add(khoa)
        await self.session.commit()
        await self.session.refresh(khoa)
        khoaResponse = map_khoa_to_response(khoa)
        return khoaResponse

    async def xoa_khoa_db(self,id:str)-> Optional[KhoaResponse]:
        stmt = (
            select(Khoa)
            .options(
                selectinload(Khoa.ds_sinh_vien)
            )
        ).where(Khoa.id==id)   
        result = await self.session.execute(stmt)    
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
        
        await self.session.delete(khoa)
        await self.session.commit()
        
        return khoaResponse