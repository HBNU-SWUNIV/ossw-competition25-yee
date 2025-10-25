from fastapi import APIRouter, HTTPException
from typing import List

router = APIRouter(prefix="/budget", tags=["budget"])


@router.get("/")
async def get_budgets():
    """예산 목록 조회"""
    return {"message": "예산 목록 조회"}


@router.post("/")
async def create_budget():
    """예산 생성"""
    return {"message": "예산 생성"}


@router.get("/{budget_id}")
async def get_budget(budget_id: str):
    """특정 예산 조회"""
    return {"message": f"예산 {budget_id} 조회"}


@router.put("/{budget_id}")
async def update_budget(budget_id: str):
    """예산 수정"""
    return {"message": f"예산 {budget_id} 수정"}


@router.delete("/{budget_id}")
async def delete_budget(budget_id: str):
    """예산 삭제"""
    return {"message": f"예산 {budget_id} 삭제"}
