from fastapi import APIRouter, HTTPException, Depends
from typing import List
from src.schemas.budget import BudgetCreate, BudgetUpdate, BudgetResponse
from src.services.budget_service import budget_service
from src.api.dependencies import get_current_user

router = APIRouter(prefix="/budget", tags=["budget"])


@router.get("/", response_model=List[BudgetResponse])
async def get_budgets(current_user: dict = Depends(get_current_user)):
    """
    예산 목록 조회

    - 사용자의 모든 예산 조회
    - spent, remaining 자동 계산
    - 조직 공유 예산의 경우 조직 멤버 전체 지출 합산
    """
    try:
        user_id = current_user["user_id"]
        organizationName = current_user.get("organizationName")
        budgets = await budget_service.get_all_budgets(user_id, organizationName)
        return budgets
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/", response_model=BudgetResponse)
async def create_budget(
    budget_data: BudgetCreate,
    current_user: dict = Depends(get_current_user)
):
    """
    예산 생성

    - name: 예산 이름
    - amount: 예산 금액
    - category: 카테고리 (선택, 기본값: 전체)
    - organizationName: 조직 이름 (선택, 공유 예산)
    """
    try:
        user_id = current_user["user_id"]
        organizationName = current_user.get("organizationName")
        budget = await budget_service.create_budget(user_id, budget_data.dict(), organizationName)
        return budget
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/migrate-to-organization")
async def migrate_budgets_to_organization(current_user: dict = Depends(get_current_user)):
    """
    기존 개인 예산을 현재 사용자의 조직 예산으로 마이그레이션
    """
    try:
        user_id = current_user["user_id"]
        organizationName = current_user.get("organizationName")
        if not organizationName:
            raise HTTPException(status_code=400, detail="조직 정보가 없습니다. 프로필에서 조직을 설정하세요.")

        updated_count = await budget_service.migrate_budgets_to_organization(user_id, organizationName)
        return {"updated": updated_count}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{budget_id}", response_model=BudgetResponse)
async def get_budget(
    budget_id: str,
    current_user: dict = Depends(get_current_user)
):
    """
    특정 예산 조회

    - spent, remaining 자동 계산
    """
    try:
        user_id = current_user["user_id"]
        budget = await budget_service.get_budget(budget_id, user_id)

        if not budget:
            raise HTTPException(status_code=404, detail="예산을 찾을 수 없습니다")

        return budget
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{budget_id}", response_model=BudgetResponse)
async def update_budget(
    budget_id: str,
    budget_data: BudgetUpdate,
    current_user: dict = Depends(get_current_user)
):
    """
    예산 수정

    - name, amount, category 수정 가능
    """
    try:
        user_id = current_user["user_id"]
        budget = await budget_service.update_budget(
            budget_id,
            user_id,
            budget_data.dict(exclude_unset=True)
        )
        return budget
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{budget_id}")
async def delete_budget(
    budget_id: str,
    current_user: dict = Depends(get_current_user)
):
    """예산 삭제"""
    try:
        user_id = current_user["user_id"]
        success = await budget_service.delete_budget(budget_id, user_id)

        if not success:
            raise HTTPException(status_code=404, detail="예산을 찾을 수 없습니다")

        return {"message": "예산이 삭제되었습니다"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
