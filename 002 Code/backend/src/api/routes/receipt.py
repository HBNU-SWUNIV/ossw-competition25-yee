from fastapi import APIRouter, UploadFile, File, HTTPException, Query
from typing import Optional, List
from datetime import datetime
from src.services.receipt_service import receipt_service
from src.schemas.receipt import ReceiptResponse

router = APIRouter(prefix="/receipt", tags=["receipt"])


@router.post("/upload")
async def upload_receipt(file: UploadFile = File(...)):
    """
    영수증 이미지 업로드 및 전체 처리

    - OCR 자동 처리
    - 카테고리 자동 분류
    - Expense 자동 생성

    **전체 플로우:**
    1. 이미지 업로드
    2. OCR 처리 (Mock 또는 실제 API)
    3. 상호명, 날짜, 품목, 금액 추출
    4. 카테고리 자동 분류
    5. 품목별 Expense 생성
    6. Receipt 저장
    """
    try:
        # TODO: 실제 사용자 ID는 인증 토큰에서 가져와야 함
        user_id = "test_user"

        # 이미지 파일 읽기
        image_data = await file.read()

        # 전체 처리 플로우 실행
        result = await receipt_service.upload_and_process_receipt(
            user_id=user_id,
            image_data=image_data,
            image_url=None  # TODO: 이미지 스토리지 업로드 후 URL 설정
        )

        return {
            "status": "success",
            "receipt_id": result["receipt"]["id"],
            "store_name": result["receipt"]["store_name"],
            "total_amount": result["receipt"]["total_amount"],
            "expenses_count": len(result["expenses"]),
            "message": result["message"]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=List[ReceiptResponse])
async def get_receipts(
    start_date: Optional[datetime] = Query(None, description="시작 날짜"),
    end_date: Optional[datetime] = Query(None, description="종료 날짜"),
    limit: int = Query(100, ge=1, le=1000, description="최대 결과 수")
):
    """영수증 목록 조회"""
    try:
        # TODO: 실제 사용자 ID는 인증 토큰에서 가져와야 함
        user_id = "test_user"

        receipts = await receipt_service.get_receipts(
            user_id=user_id,
            start_date=start_date,
            end_date=end_date,
            limit=limit
        )

        return receipts

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{receipt_id}")
async def get_receipt(receipt_id: str, include_expenses: bool = Query(False, description="관련 지출 내역 포함")):
    """
    특정 영수증 조회

    - include_expenses=true: 관련 Expense도 함께 반환
    """
    try:
        if include_expenses:
            receipt = await receipt_service.get_receipt_with_expenses(receipt_id)
        else:
            receipt = await receipt_service.get_receipt(receipt_id)

        if not receipt:
            raise HTTPException(status_code=404, detail="영수증을 찾을 수 없습니다")

        return receipt

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{receipt_id}")
async def delete_receipt(
    receipt_id: str,
    delete_expenses: bool = Query(True, description="관련 지출 내역도 함께 삭제")
):
    """
    영수증 삭제

    - delete_expenses=true: 관련 Expense도 함께 삭제 (기본값)
    - delete_expenses=false: Receipt만 삭제
    """
    try:
        success = await receipt_service.delete_receipt(receipt_id, delete_expenses=delete_expenses)

        if success:
            return {
                "message": f"영수증 {receipt_id}가 삭제되었습니다",
                "expenses_deleted": delete_expenses
            }
        else:
            raise HTTPException(status_code=404, detail="영수증을 찾을 수 없습니다")

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
