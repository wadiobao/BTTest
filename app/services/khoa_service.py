from typing import List, Optional
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import selectinload, joinedload
from sqlmodel import select
from sqlalchemy.exc import IntegrityError

from app.exceptions.CustomResponseException import CustomResponseException
from app.models.main_models import Khoa, SinhVien, LopHoc
from app.models.khoa_request import KhoaRequest
from app.models.response_models import KhoaResponse
from app.utils.mapper import map_khoa_to_response
from app.repository.khoa_repo import KhoaRepo


class KhoaService:
    def __init__(self, repo: KhoaRepo):
        self.repo = repo

    async def them_khoa_db(self, khoaRequest: KhoaRequest):
        try:
            khoa = Khoa(
                id=khoaRequest.id,
                ten_khoa=khoaRequest.ten_khoa
            )
            khoa = await self.repo.add(khoa)
            await self.repo.session.commit()
            await self.repo.session.refresh(khoa)
            # Load relationships to avoid MissingGreenlet error
            await self.repo.session.refresh(khoa, attribute_names=['ds_sinh_vien'])
            return map_khoa_to_response(khoa)
        except IntegrityError as e:
            if "Duplicate entry" in str(e):
                raise CustomResponseException(
                    message=f"Khoa với ID '{khoaRequest.id}' đã tồn tại")
            raise CustomResponseException(
                message="Có lỗi xảy ra khi thêm khoa mới")

    async def hien_ds_khoa_db(self):
        khoa_list = await self.repo.get_all()
        return [map_khoa_to_response(khoa) for khoa in khoa_list]

    async def hien_khoa_theo_id_db(self, id: str):
        khoa = await self.repo.get_by_id(id)
        if not khoa:
            raise CustomResponseException(
                message=f"Không tìm thấy khoa với ID '{id}'")
        return map_khoa_to_response(khoa)

    async def cap_nhat_khoa_db(self, id: str, khoaRequest: KhoaRequest):
        khoa = await self.repo.get_by_id(id)
        if not khoa:
            raise CustomResponseException(
                message=f"Không tìm thấy khoa với ID '{id}'")
        try:
            khoa_data = khoaRequest.model_dump(exclude_unset=True)
            khoa = await self.repo.update(id, khoa_data)
            return map_khoa_to_response(khoa)
        except IntegrityError as e:
            raise CustomResponseException(
                message="Có lỗi xảy ra khi cập nhật khoa")

    async def xoa_khoa_db(self, id: str):
        khoa = await self.repo.get_by_id(id)
        if not khoa:
            raise CustomResponseException(
                message=f"Không tìm thấy khoa với ID '{id}'")
        try:
            success = await self.repo.delete(id)
            if not success:
                raise CustomResponseException(
                    message="Không thể xóa khoa vì có sinh viên đang tham chiếu đến khoa này")
            return True
        except IntegrityError as e:
            raise CustomResponseException(
                message="Không thể xóa khoa vì có sinh viên đang tham chiếu đến khoa này")