from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class BudgetBase(BaseModel):
    """예산 기본 스키마"""
    name: str = Field(..., min_length=1, max_length=100)
    amount: float = Field(..., gt=0)
    category: str = Field(..., min_length=1, max_length=50)
    organizationName: Optional[str] = Field(None, max_length=200)


class BudgetCreate(BudgetBase):
    """예산 생성 스키마"""
    pass


class BudgetUpdate(BaseModel):
    """예산 수정 스키마"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    amount: Optional[float] = Field(None, gt=0)
    category: Optional[str] = Field(None, min_length=1, max_length=50)
    spent: Optional[float] = Field(None, ge=0)


class BudgetResponse(BudgetBase):
    """예산 응답 스키마"""
    id: str
    user_id: str
    organizationName: Optional[str] = None
    spent: float
    remaining: float
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
