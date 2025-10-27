from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class DepartmentBase(BaseModel):
    """부서 기본 스키마"""
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    budget_limit: float = Field(default=0.0, ge=0)
    manager_id: Optional[str] = None


class DepartmentCreate(DepartmentBase):
    """부서 생성 스키마"""
    pass


class DepartmentUpdate(BaseModel):
    """부서 수정 스키마"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    budget_limit: Optional[float] = Field(None, ge=0)
    manager_id: Optional[str] = None


class DepartmentResponse(DepartmentBase):
    """부서 응답 스키마"""
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
