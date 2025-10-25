from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import datetime


class ReceiptItem(BaseModel):
    """영수증 항목 스키마"""
    name: str
    price: float
    quantity: Optional[int] = 1


class ReceiptBase(BaseModel):
    """영수증 기본 스키마"""
    store_name: str = Field(..., min_length=1, max_length=100)
    total_amount: float = Field(..., gt=0)
    purchase_date: datetime
    items: List[ReceiptItem]


class ReceiptCreate(ReceiptBase):
    """영수증 생성 스키마"""
    budget_id: str


class ReceiptUpdate(BaseModel):
    """영수증 수정 스키마"""
    store_name: Optional[str] = Field(None, min_length=1, max_length=100)
    total_amount: Optional[float] = Field(None, gt=0)
    purchase_date: Optional[datetime] = None
    items: Optional[List[ReceiptItem]] = None
    budget_id: Optional[str] = None


class ReceiptResponse(ReceiptBase):
    """영수증 응답 스키마"""
    id: str
    user_id: str
    budget_id: str
    image_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class OCRResponse(BaseModel):
    """OCR 처리 결과 스키마"""
    status: str
    data: Optional[Dict] = None
    message: Optional[str] = None
