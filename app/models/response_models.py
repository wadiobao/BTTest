from typing import List, Optional
from datetime import date
from sqlmodel import SQLModel

class LopHocResponse(SQLModel):
    id: str
    ten_lop_hoc: str
    si_so: int

class SinhVienResponse(SQLModel):
    id: Optional[int] = None
    ten_sinh_vien: str
    gioi_tinh: str
    ngay_sinh: date
    sdt: str
    email: str
    que_quan: str
    khoa: Optional[str]
    ds_lop_hoc: Optional[List[LopHocResponse]] = None

class KhoaResponse(SQLModel):
    id: str
    ten_khoa: str
    ds_sinh_vien: Optional[List[SinhVienResponse]] = None 