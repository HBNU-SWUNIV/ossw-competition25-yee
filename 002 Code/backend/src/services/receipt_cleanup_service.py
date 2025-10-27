"""영수증 정리 서비스 - 자동 삭제 및 아카이브"""
from typing import Dict, Any, List
from datetime import datetime, timedelta
from src.core.firebase import firebase_client
from src.services.receipt_service import receipt_service
from src.services.expense_service import expense_service


class ReceiptCleanupService:
    """영수증 정리 및 생명주기 관리 서비스"""

    def __init__(self):
        self.db = firebase_client.db
        self.storage = firebase_client.storage

    async def cleanup_old_receipts(
        self,
        days_to_keep: int = 90,
        keep_successful_only: bool = True,
        dry_run: bool = False
    ) -> Dict[str, Any]:
        """
        오래된 영수증 정리

        Args:
            days_to_keep: 보관할 일수 (기본 90일)
            keep_successful_only: 성공한 영수증만 보관할지 여부
            dry_run: 실제 삭제하지 않고 시뮬레이션만 수행

        Returns:
            정리 결과 통계
        """
        try:
            cutoff_date = datetime.utcnow() - timedelta(days=days_to_keep)
            
            # 삭제 대상 영수증 조회
            query = self.db.collection("receipts").where("created_at", "<", cutoff_date)
            
            if keep_successful_only:
                # 실패한 영수증만 삭제 (성공한 것은 보관)
                query = query.where("ocr_status", "==", "failed")
            
            docs = query.stream()
            
            deleted_count = 0
            storage_freed = 0
            errors = []
            
            for doc in docs:
                receipt_data = doc.to_dict()
                receipt_id = doc.id
                
                try:
                    if not dry_run:
                        # 1. Storage에서 이미지 삭제
                        if receipt_data.get("image_url"):
                            try:
                                # Firebase Storage URL에서 파일 경로 추출
                                image_path = self._extract_storage_path(receipt_data["image_url"])
                                if image_path:
                                    blob = self.storage.bucket().blob(image_path)
                                    if blob.exists():
                                        storage_freed += blob.size or 0
                                        blob.delete()
                            except Exception as e:
                                print(f"Storage 삭제 실패 {receipt_id}: {e}")
                        
                        # 2. 관련 Expense는 유지 (영수증만 삭제)
                        # 또는 옵션에 따라 함께 삭제
                        
                        # 3. Firestore에서 영수증 삭제
                        doc.reference.delete()
                    
                    deleted_count += 1
                    
                except Exception as e:
                    errors.append(f"영수증 {receipt_id} 삭제 실패: {str(e)}")
            
            return {
                "status": "success",
                "deleted_count": deleted_count,
                "storage_freed_bytes": storage_freed,
                "storage_freed_mb": round(storage_freed / (1024 * 1024), 2),
                "errors": errors,
                "dry_run": dry_run,
                "cutoff_date": cutoff_date.isoformat()
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": f"정리 작업 실패: {str(e)}"
            }

    async def cleanup_failed_receipts(self, days_old: int = 7) -> Dict[str, Any]:
        """실패한 영수증들을 정리 (더 짧은 보관 기간)"""
        cutoff_date = datetime.utcnow() - timedelta(days=days_old)
        
        query = self.db.collection("receipts")\
            .where("ocr_status", "==", "failed")\
            .where("created_at", "<", cutoff_date)
        
        docs = query.stream()
        deleted_count = 0
        
        for doc in docs:
            try:
                receipt_data = doc.to_dict()
                
                # Storage 이미지 삭제
                if receipt_data.get("image_url"):
                    image_path = self._extract_storage_path(receipt_data["image_url"])
                    if image_path:
                        blob = self.storage.bucket().blob(image_path)
                        if blob.exists():
                            blob.delete()
                
                # Firestore 문서 삭제
                doc.reference.delete()
                deleted_count += 1
                
            except Exception as e:
                print(f"실패한 영수증 삭제 오류: {e}")
        
        return {
            "status": "success",
            "deleted_failed_receipts": deleted_count,
            "cutoff_date": cutoff_date.isoformat()
        }

    async def get_storage_usage_stats(self) -> Dict[str, Any]:
        """Storage 사용량 통계"""
        try:
            # 모든 영수증의 이미지 크기 합계 계산
            receipts_query = self.db.collection("receipts").stream()
            
            total_receipts = 0
            total_size_bytes = 0
            failed_receipts = 0
            
            for doc in receipts_query:
                receipt_data = doc.to_dict()
                total_receipts += 1
                
                if receipt_data.get("ocr_status") == "failed":
                    failed_receipts += 1
                
                # Storage 파일 크기 확인 (실제 구현 시 필요)
                if receipt_data.get("image_url"):
                    try:
                        image_path = self._extract_storage_path(receipt_data["image_url"])
                        if image_path:
                            blob = self.storage.bucket().blob(image_path)
                            if blob.exists():
                                total_size_bytes += blob.size or 0
                    except:
                        pass
            
            return {
                "total_receipts": total_receipts,
                "failed_receipts": failed_receipts,
                "success_receipts": total_receipts - failed_receipts,
                "total_storage_bytes": total_size_bytes,
                "total_storage_mb": round(total_size_bytes / (1024 * 1024), 2),
                "estimated_monthly_cost_usd": self._estimate_storage_cost(total_size_bytes)
            }
            
        except Exception as e:
            return {"error": f"통계 조회 실패: {str(e)}"}

    def _extract_storage_path(self, storage_url: str) -> str:
        """Firebase Storage URL에서 파일 경로 추출"""
        try:
            # Firebase Storage URL 형식: 
            # https://firebasestorage.googleapis.com/v0/b/bucket/o/path%2Fto%2Ffile?alt=media&token=...
            if "firebasestorage.googleapis.com" in storage_url:
                # URL에서 파일 경로 부분 추출
                import urllib.parse
                parts = storage_url.split("/o/")
                if len(parts) > 1:
                    encoded_path = parts[1].split("?")[0]
                    return urllib.parse.unquote(encoded_path)
            return None
        except:
            return None

    def _estimate_storage_cost(self, bytes_size: int) -> float:
        """Firebase Storage 비용 추정 (USD)"""
        # Firebase Storage 가격: $0.026 per GB/month
        gb_size = bytes_size / (1024 ** 3)
        return round(gb_size * 0.026, 4)

    async def archive_old_receipts(
        self,
        days_to_keep: int = 365,
        archive_to_cold_storage: bool = False
    ) -> Dict[str, Any]:
        """
        오래된 영수증을 아카이브 (삭제 대신 다른 컬렉션으로 이동)
        
        Args:
            days_to_keep: 메인 컬렉션에 보관할 일수
            archive_to_cold_storage: 콜드 스토리지로 이동할지 여부
        """
        cutoff_date = datetime.utcnow() - timedelta(days=days_to_keep)
        
        query = self.db.collection("receipts")\
            .where("created_at", "<", cutoff_date)\
            .where("ocr_status", "==", "completed")
        
        docs = query.stream()
        archived_count = 0
        
        for doc in docs:
            try:
                receipt_data = doc.to_dict()
                receipt_data["archived_at"] = datetime.utcnow()
                receipt_data["original_id"] = doc.id
                
                # 아카이브 컬렉션으로 이동
                self.db.collection("receipts_archive").document().set(receipt_data)
                
                # 원본 삭제
                doc.reference.delete()
                archived_count += 1
                
            except Exception as e:
                print(f"아카이브 실패: {e}")
        
        return {
            "status": "success",
            "archived_count": archived_count,
            "cutoff_date": cutoff_date.isoformat()
        }


cleanup_service = ReceiptCleanupService()