# app/services/khoa.py
from typing import List, Optional
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import selectinload, joinedload
from sqlmodel import select
from sqlalchemy.exc import IntegrityError

from app.exceptions.CustomResponseException import CustomResponseException
from app.models.MainModels import Khoa, SinhVien, LopHoc
from app.models.KhoaRequest import KhoaRequest
from app.models.response_models import KhoaResponse
from app.utils.mapper import map_khoa_to_response


class KhoaService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def them_khoa_db(self, khoaRequest: KhoaRequest):
        try:
            khoa = Khoa(
                id=khoaRequest.id,
                ten_khoa=khoaRequest.ten_khoa
            )
            self.session.add(khoa)
            await self.session.commit()
            await self.session.refresh(khoa)
            return map_khoa_to_response(khoa)
        except IntegrityError as e:
            await self.session.rollback()
            if "Duplicate entry" in str(e):
                raise CustomResponseException(
                    message=f"Khoa với ID '{khoaRequest.id}' đã tồn tại")
            raise CustomResponseException(
                message="Có lỗi xảy ra khi thêm khoa mới")

    async def hien_ds_khoa_db(self):
        statement = (
            select(Khoa)
            .options(
                selectinload(Khoa.ds_sinh_vien).selectinload(SinhVien.ds_lop_hoc)
            )
        )
        result = await self.session.execute(statement)
        khoa_list = result.scalars().all()
        return [map_khoa_to_response(khoa) for khoa in khoa_list]

    async def hien_khoa_theo_id_db(self, id: str):
        statement = (
            select(Khoa)
            .where(Khoa.id == id)
            .options(
                selectinload(Khoa.ds_sinh_vien).selectinload(SinhVien.ds_lop_hoc)
            )
        )
        result = await self.session.execute(statement)
        khoa = result.scalar_one_or_none()
        if not khoa:
            raise CustomResponseException(
                message=f"Không tìm thấy khoa với ID '{id}'")
        return map_khoa_to_response(khoa)

    async def cap_nhat_khoa_db(self, id: str, khoaRequest: KhoaRequest):
        statement = (
            select(Khoa)
            .where(Khoa.id == id)
            .options(
                selectinload(Khoa.ds_sinh_vien).selectinload(SinhVien.ds_lop_hoc)
            )
        )
        result = await self.session.execute(statement)
        khoa = result.scalar_one_or_none()
        if not khoa:
            raise CustomResponseException(
                message=f"Không tìm thấy khoa với ID '{id}'")
        try:
            khoa.ten_khoa = khoaRequest.ten_khoa
            await self.session.commit()
            await self.session.refresh(khoa)
            return map_khoa_to_response(khoa)
        except IntegrityError as e:
            await self.session.rollback()
            raise CustomResponseException(
                message="Có lỗi xảy ra khi cập nhật khoa")

    async def xoa_khoa_db(self, id: str):
        statement = select(Khoa).where(Khoa.id == id)
        result = await self.session.execute(statement)
        khoa = result.scalar_one_or_none()
        if not khoa:
            raise CustomResponseException(
                message=f"Không tìm thấy khoa với ID '{id}'")
        try:
            await self.session.delete(khoa)
            await self.session.commit()
            return True
        except IntegrityError as e:
            await self.session.rollback()
            raise CustomResponseException(
                message="Không thể xóa khoa vì có sinh viên đang tham chiếu đến khoa này")