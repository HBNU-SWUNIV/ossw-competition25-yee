"""관리자용 API - 영수증 정리 및 시스템 관리"""
from fastapi import APIRouter, HTTPException, Query, Depends
from typing import Optional
from src.services.receipt_cleanup_service import cleanup_service
from src.api.dependencies import get_current_user

router = APIRouter(prefix="/admin", tags=["admin"])


@router.post("/cleanup/receipts")
async def cleanup_old_receipts(
    days_to_keep: int = Query(90, description="보관할 일수"),
    keep_successful_only: bool = Query(True, description="성공한 영수증만 보관"),
    dry_run: bool = Query(True, description="실제 삭제하지 않고 시뮬레이션만 수행"),
    current_user: dict = Depends(get_current_user)
):
    """
    오래된 영수증 정리
    
    - 기본적으로 90일 이상 된 실패한 영수증들을 삭제
    - dry_run=True로 먼저 테스트 후 실제 삭제 수행
    """
    try:
        # 관리자 권한 확인 (필요시)
        # if current_user.get("role") != "admin":
        #     raise HTTPException(status_code=403, detail="관리자 권한이 필요합니다")
        
        result = await cleanup_service.cleanup_old_receipts(
            days_to_keep=days_to_keep,
            keep_successful_only=keep_successful_only,
            dry_run=dry_run
        )
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/cleanup/failed-receipts")
async def cleanup_failed_receipts(
    days_old: int = Query(7, description="실패한 영수증 보관 일수"),
    current_user: dict = Depends(get_current_user)
):
    """실패한 영수증들을 정리 (더 짧은 보관 기간)"""
    try:
        result = await cleanup_service.cleanup_failed_receipts(days_old=days_old)
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/storage/stats")
async def get_storage_stats(current_user: dict = Depends(get_current_user)):
    """Storage 사용량 및 비용 통계"""
    try:
        stats = await cleanup_service.get_storage_usage_stats()
        return stats
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/archive/receipts")
async def archive_old_receipts(
    days_to_keep: int = Query(365, description="메인 컬렉션에 보관할 일수"),
    current_user: dict = Depends(get_current_user)
):
    """
    오래된 영수증을 아카이브 컬렉션으로 이동
    
    - 삭제 대신 별도 컬렉션으로 이동하여 보관
    - 필요시 복구 가능
    """
    try:
        result = await cleanup_service.archive_old_receipts(days_to_keep=days_to_keep)
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/receipts/summary")
async def get_receipts_summary(current_user: dict = Depends(get_current_user)):
    """영수증 현황 요약"""
    try:
        from src.core.firebase import firebase_client
        from datetime import datetime, timedelta
        
        db = firebase_client.db
        now = datetime.utcnow()
        
        # 전체 통계
        total_receipts = len(list(db.collection("receipts").stream()))
        
        # 최근 30일 통계
        recent_date = now - timedelta(days=30)
        recent_receipts = len(list(
            db.collection("receipts")
            .where("created_at", ">=", recent_date)
            .stream()
        ))
        
        # 실패한 영수증 통계
        failed_receipts = len(list(
            db.collection("receipts")
            .where("ocr_status", "==", "failed")
            .stream()
        ))
        
        # 오래된 영수증 (90일 이상)
        old_date = now - timedelta(days=90)
        old_receipts = len(list(
            db.collection("receipts")
            .where("created_at", "<", old_date)
            .stream()
        ))
        
        return {
            "total_receipts": total_receipts,
            "recent_receipts_30days": recent_receipts,
            "failed_receipts": failed_receipts,
            "old_receipts_90days": old_receipts,
            "success_rate": round((total_receipts - failed_receipts) / total_receipts * 100, 2) if total_receipts > 0 else 0,
            "cleanup_recommended": old_receipts > 100 or failed_receipts > 50
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))