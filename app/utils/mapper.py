

from app.models.KhoaResponse import KhoaResponse
from app.models.LopHocResponse import LopHocResponse
from app.models.MainModels import Khoa, LopHoc, SinhVien
from app.models.SinhVienResponse import SinhVienResponse

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
    