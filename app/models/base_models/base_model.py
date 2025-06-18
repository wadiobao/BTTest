from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel

class TimeStampedModel(SQLModel):
    created_at: datetime = Field(
        default_factory=datetime.utcnow, 
        nullable=False,
        description="Thời điểm bản ghi được tạo"
    )
    
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        sa_column_kwargs={"onupdate": datetime.utcnow},
        description="Thời điểm bản ghi được cập nhật lần cuối"
    )

    deleted_at: Optional[datetime] = Field(
        default=None, 
        nullable=True, 
        index=True,  # Đánh index để truy vấn các bản ghi đã/chưa xóa nhanh hơn
        description="Thời điểm bản ghi bị xóa mềm"
    )
