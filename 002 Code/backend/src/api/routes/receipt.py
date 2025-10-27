from fastapi import APIRouter, UploadFile, File, HTTPException, Query, Depends
from typing import Optional, List
from datetime import datetime
from src.services.receipt_service import receipt_service
from src.schemas.receipt import ReceiptResponse
from src.api.dependencies import get_current_user

router = APIRouter(prefix="/receipt", tags=["receipt"])


@router.post("/ocr")
async def ocr_receipt(
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user)
):
    """
    영수증 이미지 OCR 처리만 수행 (Expense 생성 안함)

    - OCR 처리하여 영수증 정보 추출
    - Receipt는 저장하지만 Expense는 생성하지 않음
    - 프론트엔드에서 "등록" 버튼 클릭 시 Expense 생성

    **플로우:**
    1. 이미지 업로드
    2. OCR 처리
    3. 상호명, 주소, 전화번호, 날짜, 금액 추출
    4. Receipt 정보만 반환 (DB 저장 안함)
    """
    try:
        # 인증된 사용자 ID 가져오기
        user_id = current_user["user_id"]

        # 이미지 파일 읽기
        image_data = await file.read()

        # OCR만 수행
        from src.services.ocr_service import ocr_service
        ocr_result = await ocr_service.process_receipt(image_data=image_data)

        if ocr_result["status"] != "success":
            raise HTTPException(status_code=400, detail=f"OCR 처리 실패: {ocr_result.get('message', 'Unknown error')}")

        ocr_data = ocr_result["data"]

        # 날짜를 YYYY-MM-DD 형식으로 변환
        date_value = ocr_data.get("date")
        if isinstance(date_value, datetime):
            date_str = date_value.strftime("%Y-%m-%d")
        else:
            date_str = str(date_value) if date_value else ""

        return {
            "status": "success",
            "data": {
                "store_name": ocr_data.get("store_name", ""),
                "store_address": ocr_data.get("store_address", ""),
                "store_phone_number": ocr_data.get("store_phone_number", ""),
                "date": date_str,
                "total_amount": ocr_data.get("total_amount", 0)
            }
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/upload")
async def upload_receipt(
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user)
):
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
        # 인증된 사용자 ID 가져오기
        user_id = current_user["user_id"]

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
    limit: int = Query(100, ge=1, le=1000, description="최대 결과 수"),
    current_user: dict = Depends(get_current_user)
):
    """영수증 목록 조회"""
    try:
        # 인증된 사용자 ID 가져오기
        user_id = current_user["user_id"]

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
