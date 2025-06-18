from typing import List, Optional
from sqlalchemy.exc import IntegrityError

from app.exceptions.CustomResponseException import CustomResponseException
from app.models.main_models import LopHoc
from app.models.lop_hoc_request import LopHocRequest
from app.models.response_models import LopHocResponse
from app.utils.mapper import map_lop_hoc_to_response
from app.repository.lop_hoc_repo import LopHocRepo


class LopHocService:
    def __init__(self, repo: LopHocRepo):
        self.repo = repo

    async def them_lop_hoc_db(self, lop_hoc_request: LopHocRequest):
        try:
            lop_hoc = LopHoc(
                id=lop_hoc_request.id,
                ten_lop_hoc=lop_hoc_request.ten_lop_hoc,
                si_so=lop_hoc_request.si_so
            )
            lop_hoc = await self.repo.add(lop_hoc)
            return map_lop_hoc_to_response(lop_hoc)
        except IntegrityError as e:
            if "Duplicate entry" in str(e):
                raise CustomResponseException(
                    message=f"Lớp học với ID '{lop_hoc_request.id}' đã tồn tại")
            raise CustomResponseException(
                message="Có lỗi xảy ra khi thêm lớp học mới")

    async def hien_ds_lop_hoc_db(self):
        lop_hoc_list = await self.repo.get_all()
        return [map_lop_hoc_to_response(lop_hoc) for lop_hoc in lop_hoc_list]

    async def hien_lop_hoc_theo_id_db(self, id: str):
        lop_hoc = await self.repo.get_by_id(id)
        if not lop_hoc:
            raise CustomResponseException(
                message=f"Không tìm thấy lớp học với ID '{id}'")
        return map_lop_hoc_to_response(lop_hoc)

    async def cap_nhat_lop_hoc_db(self, id: str, lop_hoc_request: LopHocRequest):
        lop_hoc = await self.repo.get_by_id(id)
        if not lop_hoc:
            raise CustomResponseException(
                message=f"Không tìm thấy lớp học với ID '{id}'")
        try:
            lop_hoc_data = lop_hoc_request.model_dump(exclude_unset=True)
            lop_hoc = await self.repo.update(id, lop_hoc_data)
            return map_lop_hoc_to_response(lop_hoc)
        except IntegrityError as e:
            raise CustomResponseException(
                message="Có lỗi xảy ra khi cập nhật lớp học")

    async def xoa_lop_hoc_db(self, id: str):
        lop_hoc = await self.repo.get_by_id(id)
        if not lop_hoc:
            raise CustomResponseException(
                message=f"Không tìm thấy lớp học với ID '{id}'")
        try:
            success = await self.repo.delete(id)
            if not success:
                raise CustomResponseException(
                    message="Không thể xóa lớp học vì có sinh viên đang tham chiếu đến lớp học này")
            return True
        except IntegrityError as e:
            raise CustomResponseException(
                message="Không thể xóa lớp học vì có sinh viên đang tham chiếu đến lớp học này")