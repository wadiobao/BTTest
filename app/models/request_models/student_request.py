import re
from typing import Optional
from datetime import date
from sqlmodel import SQLModel
from pydantic import field_validator

from app.exceptions import ResponseException

class StudentRequest(SQLModel):
    """Request model for student operations"""
    name: Optional[str] = None
    gender: Optional[str] = None
    birth_date: Optional[date] = None
    phone: Optional[str] = None
    email: str
    hometown: Optional[str] = None
    faculty_id: Optional[str] = None
    
    class Config:
        orm_mode = True
    
    @field_validator("gender")
    def validate_gender(cls, v):
        if v and v.lower() not in ("nam", "nữ", "nu"):
            raise ResponseException(
                message="Giới tính phải là 'Nam' hoặc 'Nữ'"
            )
        return v.title() if v else v
    
    @field_validator("phone")
    def validate_phone(cls, v):
        if v and not re.match(r"^(0|\+84)[0-9]{9}$", v):
            raise ResponseException(
                message="Số điện thoại không hợp lệ")
        return v
    
    @field_validator("birth_date", mode="after")
    @classmethod
    def validate_birth_date(cls, v: Optional[date]):
        if v:
            today = date.today()
            age = today.year - v.year - ((today.month, today.day) < (v.month, v.day))
            if age <= 18:
                raise ResponseException(
                    message="Sinh viên phải đủ 18 tuổi trở lên.")
        return v
    
    @field_validator('email')
    @classmethod
    def validate_email_format(cls, v: str) -> str:
        email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.fullmatch(email_regex, v):
            raise ResponseException(
                message="Email không hợp lệ. Vui lòng nhập email đúng định dạng.")
        return v 
