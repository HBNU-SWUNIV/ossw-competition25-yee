from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    """사용자 기본 스키마"""
    email: EmailStr
    name: str = Field(..., min_length=1, max_length=100)


class UserCreate(UserBase):
    """사용자 생성 스키마 (회원가입)"""
    password: str = Field(..., min_length=8, max_length=100)


class UserLogin(BaseModel):
    """사용자 로그인 스키마"""
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    """사용자 정보 수정 스키마"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    password: Optional[str] = Field(None, min_length=8, max_length=100)


class UserResponse(UserBase):
    """사용자 응답 스키마"""
    id: str
    role: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    """토큰 응답 스키마"""
    access_token: str
    token_type: str = "bearer"
