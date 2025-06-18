from typing import Any, List, Optional, Set
from pydantic import BaseModel, EmailStr, Field, HttpUrl, field_validator, validator
from sqlalchemy import URL
from sqlmodel import Field, Relationship, SQLModel, extract, select 

class ResponseException(Exception):
    """Custom exception for API responses"""
    message: str
    
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)
        
class ApiResponse(BaseModel):
    """Standard API response model"""
    code: int
    status: str = Field(default="success")
    result: Any 