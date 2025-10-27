from fastapi import APIRouter, HTTPException, Query, Depends
from fastapi.responses import Response
from typing import Optional, List
from datetime import datetime
from src.schemas.expense import (
    ExpenseCreate,
    ExpenseUpdate,
    ExpenseResponse,
    ExpenseSummary
)
from src.services.expense_service import expense_service
from src.services.receipt_service import receipt_service
from src.services.pdf_service import pdf_service
from src.api.dependencies import get_current_user

router = APIRouter(prefix="/expense", tags=["expense"])


@router.post("/", response_model=ExpenseResponse)
async def create_expense(
    expense_data: ExpenseCreate,
    current_user: dict = Depends(get_current_user)
):
    """
    지출 내역 생성

    - 카테고리가 지정되지 않으면 자동으로 분류됩니다
    """
    try:
        # 인증된 사용자 ID 가져오기
        user_id = current_user["user_id"]

        expense = await expense_service.create_expense(
            user_id=user_id,
            receipt_id=expense_data.receipt_id,
            store_name=expense_data.store_name,
            amount=expense_data.amount,
            date=expense_data.date,
            store_address=expense_data.store_address,
            store_phone_number=expense_data.store_phone_number,
            item_name=expense_data.item_name,
            category=expense_data.category,
            description=expense_data.description
        )

        return expense
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=List[ExpenseResponse])
async def get_expenses(
    category: Optional[str] = Query(None, description="카테고리 필터"),
    start_date: Optional[datetime] = Query(None, description="시작 날짜"),
    end_date: Optional[datetime] = Query(None, description="종료 날짜"),
    limit: int = Query(100, ge=1, le=1000, description="최대 결과 수"),
    current_user: dict = Depends(get_current_user)
):
    """
    지출 내역 목록 조회

    - 카테고리, 날짜 범위로 필터링 가능
    """
    try:
        # 인증된 사용자 ID 가져오기
        user_id = current_user["user_id"]

        expenses = await expense_service.get_expenses(
            user_id=user_id,
            category=category,
            start_date=start_date,
            end_date=end_date,
            limit=limit
        )

        return expenses
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/statistics", response_model=ExpenseSummary)
async def get_expense_statistics(
    start_date: Optional[datetime] = Query(None, description="시작 날짜 (기본: 이번 달 1일)"),
    end_date: Optional[datetime] = Query(None, description="종료 날짜 (기본: 오늘)"),
    current_user: dict = Depends(get_current_user)
):
    """
    지출 통계 조회 (재무제표용)

    - 카테고리별 금액, 건수, 비율을 반환합니다
    """
    try:
        # 인증된 사용자 ID 가져오기
        user_id = current_user["user_id"]

        statistics = await expense_service.get_statistics(
            user_id=user_id,
            start_date=start_date,
            end_date=end_date
        )

        return statistics
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/by-receipt/{receipt_id}", response_model=List[ExpenseResponse])
async def get_expenses_by_receipt(receipt_id: str):
    """
    특정 영수증의 모든 지출 내역 조회
    """
    try:
        expenses = await expense_service.get_expenses_by_receipt(receipt_id)
        return expenses
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{expense_id}", response_model=ExpenseResponse)
async def get_expense(expense_id: str):
    """특정 지출 내역 조회"""
    try:
        expense = await expense_service.get_expense(expense_id)

        if not expense:
            raise HTTPException(status_code=404, detail="지출 내역을 찾을 수 없습니다")

        return expense
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{expense_id}", response_model=ExpenseResponse)
async def update_expense(expense_id: str, expense_data: ExpenseUpdate):
    """
    지출 내역 수정

    - 카테고리를 수동으로 변경할 수 있습니다
    """
    try:
        # 수정할 데이터만 딕셔너리로 변환
        update_data = expense_data.model_dump(exclude_unset=True)

        if not update_data:
            raise HTTPException(status_code=400, detail="수정할 데이터가 없습니다")

        expense = await expense_service.update_expense(expense_id, update_data)
        return expense
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{expense_id}")
async def delete_expense(expense_id: str):
    """지출 내역 삭제"""
    try:
        success = await expense_service.delete_expense(expense_id)

        if success:
            return {"message": f"지출 내역 {expense_id}가 삭제되었습니다"}
        else:
            raise HTTPException(status_code=404, detail="지출 내역을 찾을 수 없습니다")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{expense_id}/pdf")
async def export_expense_pdf(expense_id: str):
    """
    개별 지출 내역 PDF 내보내기

    영수증 이미지, 상호명, 주소, 전화번호, 날짜, 총액 등이 포함된 PDF 생성
    """
    try:
        # 지출 내역 조회
        expense = await expense_service.get_expense(expense_id)
        if not expense:
            raise HTTPException(status_code=404, detail="지출 내역을 찾을 수 없습니다")

        # 영수증 조회 (이미지 포함)
        receipt = None
        if expense.get("receipt_id"):
            receipt = await receipt_service.get_receipt(expense["receipt_id"])

        # PDF 생성
        pdf_bytes = await pdf_service.generate_expense_pdf(expense, receipt)

        # PDF 파일명 생성
        date_str = expense.get('date', datetime.now()).strftime('%Y%m%d') if isinstance(expense.get('date'), datetime) else datetime.now().strftime('%Y%m%d')
        store_name = expense.get('store_name', 'expense')
        filename = f"expense_{store_name}_{date_str}.pdf"

        # PDF 응답 반환
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename={filename}"
            }
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF 생성 실패: {str(e)}")
