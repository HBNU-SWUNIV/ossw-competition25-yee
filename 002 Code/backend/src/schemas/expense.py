from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ExpenseBase(BaseModel):
    """지출 기본 스키마"""
    category: str = Field(..., min_length=1, max_length=50)
    amount: float = Field(..., gt=0)
    date: datetime
    store_name: str = Field(..., min_length=1, max_length=100)
    store_address: Optional[str] = Field(None, max_length=200)
    store_phone_number: Optional[str] = Field(None, max_length=50)
    description: Optional[str] = Field(None, max_length=500)
    item_name: Optional[str] = Field(None, max_length=200)


class ExpenseCreate(ExpenseBase):
    """지출 생성 스키마"""
    receipt_id: str


class ExpenseUpdate(BaseModel):
    """지출 수정 스키마"""
    category: Optional[str] = Field(None, min_length=1, max_length=50)
    amount: Optional[float] = Field(None, gt=0)
    date: Optional[datetime] = None
    store_name: Optional[str] = Field(None, min_length=1, max_length=100)
    store_address: Optional[str] = Field(None, max_length=200)
    store_phone_number: Optional[str] = Field(None, max_length=50)
    description: Optional[str] = Field(None, max_length=500)
    item_name: Optional[str] = Field(None, max_length=200)


class ExpenseResponse(ExpenseBase):
    """지출 응답 스키마"""
    id: str
    user_id: str
    receipt_id: str
    classification_method: str
    classification_confidence: Optional[float] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ExpenseStatistics(BaseModel):
    """지출 통계 스키마 (재무제표용)"""
    category: str
    total_amount: float
    count: int
    percentage: float


class ExpenseSummary(BaseModel):
    """전체 지출 요약"""
    total_amount: float
    total_count: int
    by_category: list[ExpenseStatistics]
    start_date: datetime
    end_date: datetime
