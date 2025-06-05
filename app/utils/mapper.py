from app.models.MainModels import Khoa, SinhVien, LopHoc
from app.models.response_models import KhoaResponse, SinhVienResponse, LopHocResponse
from datetime import datetime

def map_lop_to_response(lopHoc: LopHoc) -> LopHocResponse:
    return LopHocResponse(
        id=lopHoc.id,
        ten_lop_hoc=lopHoc.ten_lop_hoc,
        si_so=lopHoc.si_so
    )

def map_sinhvien_to_response(sinhVien: SinhVien) -> SinhVienResponse:
    return SinhVienResponse(
        id=sinhVien.id,
        ten_sinh_vien=sinhVien.ten_sinh_vien,
        gioi_tinh=sinhVien.gioi_tinh,
        ngay_sinh=sinhVien.ngay_sinh.date() if isinstance(sinhVien.ngay_sinh, datetime) else sinhVien.ngay_sinh,
        sdt=sinhVien.sdt,
        email=sinhVien.email,
        que_quan=sinhVien.que_quan,
        khoa=sinhVien.khoa.ten_khoa if sinhVien.khoa else None,
        ds_lop_hoc=[map_lop_to_response(lh) for lh in sinhVien.ds_lop_hoc] if hasattr(sinhVien, 'ds_lop_hoc') and sinhVien.ds_lop_hoc else None
    )

def map_khoa_to_response(khoa: Khoa) -> KhoaResponse:
    return KhoaResponse(
        id=khoa.id,
        ten_khoa=khoa.ten_khoa,
        ds_sinh_vien=[map_sinhvien_to_response(sv) for sv in khoa.ds_sinh_vien] if hasattr(khoa, 'ds_sinh_vien') and khoa.ds_sinh_vien else None
    )
    