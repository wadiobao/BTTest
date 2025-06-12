from datetime import datetime
from typing import List
from sqlalchemy import extract, select
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.main_models import Khoa
from app.repository.i_khoa_repo import IKhoaRepo


class KhoaRepo(IKhoaRepo):
    
    def __init__(self, session:AsyncSession):
        self.session = session
        
    async def check_existed(self,id:int) -> bool:
        query = select(Khoa).where(Khoa.id == id).exists()
        result = await self.session.execute(select(query))
        return result.scalar()