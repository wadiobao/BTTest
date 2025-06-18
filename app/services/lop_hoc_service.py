from typing import List, Optional
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from app.exceptions import ResponseException
from app.models.base_models import Faculty, Student, Class
from app.models.request_models import ClassRequest
from app.models.response_models import LopHocResponse
from app.utils.mapper import map_lop_hoc_to_response
from app.repository.class_repo import ClassRepo


class LopHocService:
    def __init__(self, repo: ClassRepo):
        self.repo = repo

    async def them_lop_hoc_db(self, lop_hoc_request: ClassRequest):
        try:
            lop_hoc = Class(
                id=lop_hoc_request.id,
                name=lop_hoc_request.name,
                capacity=lop_hoc_request.capacity
            )
            lop_hoc = await self.repo.add(lop_hoc)
            return map_lop_hoc_to_response(lop_hoc)
        except IntegrityError as e:
            if "Duplicate entry" in str(e):
                raise ResponseException(
                    message=f"Lớp học với ID '{lop_hoc_request.id}' đã tồn tại")
            raise ResponseException(
                message="Có lỗi xảy ra khi thêm lớp học mới")

    async def hien_ds_lop_hoc_db(self):
        lop_hoc_list = await self.repo.get_all()
        return [map_lop_hoc_to_response(lop_hoc) for lop_hoc in lop_hoc_list]

    async def hien_lop_hoc_theo_id_db(self, id: str):
        lop_hoc = await self.repo.get_by_id(id)
        if not lop_hoc:
            raise ResponseException(
                message=f"Không tìm thấy lớp học với ID '{id}'")
        return map_lop_hoc_to_response(lop_hoc)

    async def cap_nhat_lop_hoc_db(self, id: str, lop_hoc_request: ClassRequest):
        lop_hoc = await self.repo.get_by_id(id)
        if not lop_hoc:
            raise ResponseException(
                message=f"Không tìm thấy lớp học với ID '{id}'")
        try:
            lop_hoc_data = lop_hoc_request.model_dump(exclude_unset=True)
            lop_hoc = await self.repo.update(id, lop_hoc_data)
            return map_lop_hoc_to_response(lop_hoc)
        except IntegrityError as e:
            raise ResponseException(
                message="Có lỗi xảy ra khi cập nhật lớp học")

    async def xoa_lop_hoc_db(self, id: str):
        lop_hoc = await self.repo.get_by_id(id)
        if not lop_hoc:
            raise ResponseException(
                message=f"Không tìm thấy lớp học với ID '{id}'")
        try:
            success = await self.repo.delete(id)
            if not success:
                raise ResponseException(
                    message="Không thể xóa lớp học vì có sinh viên đang tham chiếu đến lớp học này")
            return True
        except IntegrityError as e:
            raise ResponseException(
                message="Không thể xóa lớp học vì có sinh viên đang tham chiếu đến lớp học này")
