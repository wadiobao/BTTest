from typing import List, Optional
from datetime import date, datetime
from sqlmodel import Field, Relationship, SQLModel

class Khoa(SQLModel, table=True):
    id: Optional[str] = Field(default=None, primary_key=True)
    ten_khoa: str = Field(index=True)
    
    ds_sinh_vien: List["SinhVien"] = Relationship(back_populates="khoa")

class SinhVienLopHoc(SQLModel, table=True):
    sinh_vien_id: Optional[int] = Field(default=None, foreign_key="sinhvien.id", primary_key=True)
    lop_hoc_id: Optional[str] = Field(default=None, foreign_key="lophoc.id", primary_key=True)

class SinhVien(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    ten_sinh_vien: str = Field(index=True)
    gioi_tinh: str
    ngay_sinh: date 
    sdt: str
    email: str
    que_quan: str
    
    khoa_id: Optional[str] = Field(default=None, foreign_key="khoa.id", nullable=True)
    khoa: Optional[Khoa] = Relationship(back_populates="ds_sinh_vien")
    
    ds_lop_hoc: List["LopHoc"] = Relationship(back_populates="ds_sinh_vien", link_model=SinhVienLopHoc)

class LopHoc(SQLModel, table=True):
    id: Optional[str] = Field(default=None, primary_key=True)
    ten_lop_hoc: str = Field(index=True)
    si_so: int = Field(default=None) 
    
    ds_sinh_vien: List["SinhVien"] = Relationship(back_populates="ds_lop_hoc", link_model=SinhVienLopHoc)