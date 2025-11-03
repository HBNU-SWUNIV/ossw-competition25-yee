from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from typing import Dict
from src.api.dependencies import get_current_user
from src.core.firebase import firebase_client
import uuid


router = APIRouter(prefix="/report", tags=["report"])


@router.post("/upload", response_model=Dict[str, str])
async def upload_report_pdf(
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user)
):
    """
    PDF를 Firebase Storage에 업로드하고 공개 URL을 반환합니다.
    """
    try:
        content = await file.read()
        if not content:
            raise HTTPException(status_code=400, detail="빈 파일입니다")

        bucket = firebase_client.bucket
        if not bucket:
            raise HTTPException(status_code=500, detail="Firebase Storage가 설정되지 않았습니다")

        org = current_user.get("organizationName") or "unknown"
        filename = file.filename or f"{uuid.uuid4()}.pdf"
        blob_path = f"reports/{org}/{filename}"
        blob = bucket.blob(blob_path)
        blob.upload_from_string(content, content_type="application/pdf")
        blob.make_public()
        return {"url": blob.public_url}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


