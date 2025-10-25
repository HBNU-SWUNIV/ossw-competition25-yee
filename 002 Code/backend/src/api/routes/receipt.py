from fastapi import APIRouter, UploadFile, File, HTTPException

router = APIRouter(prefix="/receipt", tags=["receipt"])


@router.post("/upload")
async def upload_receipt(file: UploadFile = File(...)):
    """영수증 이미지 업로드 및 OCR 처리"""
    return {"message": "영수증 업로드 및 OCR 처리"}


@router.get("/")
async def get_receipts():
    """영수증 목록 조회"""
    return {"message": "영수증 목록 조회"}


@router.get("/{receipt_id}")
async def get_receipt(receipt_id: str):
    """특정 영수증 조회"""
    return {"message": f"영수증 {receipt_id} 조회"}


@router.put("/{receipt_id}")
async def update_receipt(receipt_id: str):
    """영수증 정보 수정"""
    return {"message": f"영수증 {receipt_id} 수정"}


@router.delete("/{receipt_id}")
async def delete_receipt(receipt_id: str):
    """영수증 삭제"""
    return {"message": f"영수증 {receipt_id} 삭제"}
