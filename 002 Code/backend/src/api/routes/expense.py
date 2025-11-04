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
            description=expense_data.description,
            budget_id=expense_data.budget_id
        )

        return expense
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=List[ExpenseResponse])
async def get_expenses(
    category: Optional[str] = Query(None, description="카테고리 필터"),
    start_date: Optional[str] = Query(None, description="시작 날짜"),
    end_date: Optional[str] = Query(None, description="종료 날짜"),
    limit: int = Query(100, ge=1, le=10000, description="최대 결과 수"),
    current_user: dict = Depends(get_current_user)
):
    """
    지출 내역 목록 조회

    - 카테고리, 날짜 범위로 필터링 가능
    - 조직 공유 지출인 경우 조직 멤버 전체 지출 조회
    """
    try:
        # 인증된 사용자 ID 가져오기
        user_id = current_user["user_id"]
        organizationName = current_user.get("organizationName")

        # 문자열 날짜를 datetime으로 파싱
        parsed_start_date = None
        parsed_end_date = None
        if start_date:
            try:
                parsed_start_date = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
            except ValueError:
                raise HTTPException(status_code=400, detail="잘못된 start_date 형식")
        if end_date:
            try:
                parsed_end_date = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
            except ValueError:
                raise HTTPException(status_code=400, detail="잘못된 end_date 형식")

        expenses = await expense_service.get_expenses(
            user_id=user_id,
            category=category,
            start_date=parsed_start_date,
            end_date=parsed_end_date,
            limit=limit,
            organizationName=organizationName
        )

        return expenses
    except HTTPException:
        raise
    except Exception as e:
        print(f"[ERROR] get_expenses 실패: {str(e)}")
        import traceback
        traceback.print_exc()
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
    - 조직 공유 지출인 경우 조직 멤버 전체 지출 통계
    """
    try:
        # 인증된 사용자 ID 가져오기
        user_id = current_user["user_id"]
        organizationName = current_user.get("organizationName")

        statistics = await expense_service.get_statistics(
            user_id=user_id,
            start_date=start_date,
            end_date=end_date,
            organizationName=organizationName
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


@router.post("/report/pdf")
async def export_report_pdf(
    expense_ids: List[str],
    current_user: dict = Depends(get_current_user)
):
    """
    선택된 지출 내역들의 리포트 PDF 생성
    
    Args:
        expense_ids: 지출 내역 ID 리스트
    """
    try:
        print(f"[PDF] 리포트 생성 요청 받음, expense_ids: {expense_ids}")

        if not expense_ids:
            raise HTTPException(status_code=400, detail="선택된 지출 내역이 없습니다")

        # 지출 내역들 조회 및 영수증 이미지 URL 추가
        expenses = []
        for expense_id in expense_ids:
            print(f"[PDF] 지출 내역 조회 중: {expense_id}")
            expense = await expense_service.get_expense(expense_id)
            if expense:
                # receipt_id로 영수증 조회하여 image_url 추가
                receipt_id = expense.get('receipt_id')
                if receipt_id:
                    print(f"[PDF] 영수증 조회 중: {receipt_id}")
                    receipt = await receipt_service.get_receipt(receipt_id)

                    if receipt and receipt.get('image_url'):
                        expense['receipt_url'] = receipt.get('image_url')
                        print(f"[PDF] 영수증 이미지 URL 추가: {receipt.get('image_url')}")
                    elif receipt_id.startswith('manual-'):
                        # manual receipt인 경우 자동 매칭 시도
                        print(f"[PDF] Manual receipt 감지 - 자동 매칭 시도")
                        expense_date = expense.get('date')
                        if isinstance(expense_date, str):
                            try:
                                expense_date = datetime.fromisoformat(expense_date.replace('Z', '+00:00'))
                            except:
                                expense_date = datetime.utcnow()

                        matched_receipt = await receipt_service.find_matching_receipt(
                            user_id=expense.get('user_id'),
                            store_name=expense.get('store_name', ''),
                            amount=expense.get('amount', 0),
                            date=expense_date
                        )

                        if matched_receipt and matched_receipt.get('image_url'):
                            expense['receipt_url'] = matched_receipt.get('image_url')
                            print(f"[PDF] 매칭된 영수증 이미지 URL 추가: {matched_receipt.get('image_url')}")
                        else:
                            print(f"[PDF] 매칭되는 영수증 없음")
                            expense['receipt_url'] = None
                    else:
                        print(f"[PDF] 영수증 이미지 없음")
                        expense['receipt_url'] = None
                else:
                    print(f"[PDF] receipt_id 없음")
                    expense['receipt_url'] = None

                expenses.append(expense)
                print(f"[PDF] 지출 내역 추가: {expense.get('store_name', 'N/A')}")

        if not expenses:
            raise HTTPException(status_code=404, detail="유효한 지출 내역을 찾을 수 없습니다")

        print(f"[PDF] 총 {len(expenses)}개 지출 내역으로 PDF 생성 시작")

        # 리포트 PDF 생성
        pdf_bytes = await pdf_service.generate_report_pdf(expenses)

        print(f"[PDF] PDF 생성 완료, 크기: {len(pdf_bytes)} bytes")

        # 파일명 생성
        today = datetime.now().strftime('%Y%m%d')
        filename = f"expense_report_{today}.pdf"

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
        print(f"[PDF] 에러 발생: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"리포트 PDF 생성 실패: {str(e)}")
