from typing import Dict, Any, List, Optional
from datetime import datetime
from src.core.firebase import firebase_client
from src.services.ocr_service import ocr_service
from src.services.expense_service import expense_service
from src.services.category_service import category_service


class ReceiptService:
    """영수증 관리 서비스 (OCR + Expense 통합)"""

    def __init__(self):
        self.db = firebase_client.db
        self.collection = "receipts"

    async def upload_and_process_receipt(
        self,
        user_id: str,
        image_data: bytes = None,
        image_url: str = None
    ) -> Dict[str, Any]:
        """
        영수증 업로드 및 전체 처리 플로우

        1. 이미지 업로드
        2. OCR 처리
        3. 데이터 추출
        4. 카테고리 자동 분류
        5. Expense 자동 생성
        6. Receipt 저장

        Args:
            user_id: 사용자 ID
            image_data: 이미지 바이트 데이터
            image_url: 이미지 URL (선택)

        Returns:
            처리 결과 (receipt, expenses)
        """
        try:
            # 1. OCR 처리
            print(f"📷 영수증 OCR 처리 시작...")
            ocr_result = await ocr_service.process_receipt(image_data=image_data)

            if ocr_result["status"] != "success":
                raise Exception(f"OCR 처리 실패: {ocr_result.get('message', 'Unknown error')}")

            ocr_data = ocr_result["data"]

            # 2. Receipt 데이터 생성
            receipt_data = {
                "user_id": user_id,
                "store_name": ocr_data["store_name"],
                "total_amount": ocr_data["total_amount"],
                "purchase_date": datetime.strptime(ocr_data["date"], "%Y-%m-%d"),
                "items": ocr_data["items"],
                "image_url": image_url,
                "ocr_raw_data": ocr_result.get("raw_ocr_response"),
                "ocr_status": "completed",
                "ocr_processed_at": datetime.utcnow(),
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }

            # 3. Firestore에 Receipt 저장
            receipt_ref = self.db.collection(self.collection).document()
            receipt_ref.set(receipt_data)
            receipt_data["id"] = receipt_ref.id

            print(f"✅ Receipt 저장 완료: {receipt_ref.id}")

            # 4. 각 품목별로 Expense 자동 생성
            created_expenses = []

            for item in ocr_data["items"]:
                # 카테고리 자동 분류
                category, confidence = category_service.classify(
                    store_name=ocr_data["store_name"],
                    item_name=item["name"],
                    amount=item["price"]
                )

                # Expense 생성
                expense = await expense_service.create_expense(
                    user_id=user_id,
                    receipt_id=receipt_ref.id,
                    store_name=ocr_data["store_name"],
                    amount=item["price"],
                    date=receipt_data["purchase_date"],
                    item_name=item["name"],
                    category=category,
                    description=f"{ocr_data['store_name']}에서 구매"
                )

                created_expenses.append(expense)
                print(f"💰 Expense 생성: {item['name']} - {category} - {item['price']}원")

            return {
                "status": "success",
                "receipt": receipt_data,
                "expenses": created_expenses,
                "message": f"영수증 처리 완료: {len(created_expenses)}개의 지출 내역이 생성되었습니다"
            }

        except Exception as e:
            # 에러 발생 시 Receipt는 failed 상태로 저장
            error_receipt_data = {
                "user_id": user_id,
                "store_name": "",
                "total_amount": 0,
                "purchase_date": datetime.utcnow(),
                "items": [],
                "image_url": image_url,
                "ocr_status": "failed",
                "ocr_raw_data": {"error": str(e)},
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }

            receipt_ref = self.db.collection(self.collection).document()
            receipt_ref.set(error_receipt_data)

            raise Exception(f"영수증 처리 실패: {str(e)}")

    async def get_receipts(
        self,
        user_id: str,
        start_date: datetime = None,
        end_date: datetime = None,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """영수증 목록 조회"""
        try:
            query = self.db.collection(self.collection).where("user_id", "==", user_id)

            if start_date:
                query = query.where("purchase_date", ">=", start_date)
            if end_date:
                query = query.where("purchase_date", "<=", end_date)

            query = query.order_by("purchase_date", direction="DESCENDING").limit(limit)

            docs = query.stream()
            receipts = []
            for doc in docs:
                receipt_data = doc.to_dict()
                receipt_data["id"] = doc.id
                receipts.append(receipt_data)

            return receipts

        except Exception as e:
            raise Exception(f"영수증 목록 조회 실패: {str(e)}")

    async def get_receipt(self, receipt_id: str) -> Optional[Dict[str, Any]]:
        """특정 영수증 조회"""
        try:
            doc = self.db.collection(self.collection).document(receipt_id).get()

            if doc.exists:
                receipt_data = doc.to_dict()
                receipt_data["id"] = doc.id
                return receipt_data
            return None

        except Exception as e:
            raise Exception(f"영수증 조회 실패: {str(e)}")

    async def get_receipt_with_expenses(self, receipt_id: str) -> Optional[Dict[str, Any]]:
        """영수증과 관련 지출 내역을 함께 조회"""
        try:
            receipt = await self.get_receipt(receipt_id)

            if not receipt:
                return None

            # 관련 Expense 조회
            expenses = await expense_service.get_expenses_by_receipt(receipt_id)

            receipt["expenses"] = expenses
            return receipt

        except Exception as e:
            raise Exception(f"영수증 상세 조회 실패: {str(e)}")

    async def delete_receipt(self, receipt_id: str, delete_expenses: bool = True) -> bool:
        """
        영수증 삭제

        Args:
            receipt_id: 영수증 ID
            delete_expenses: 관련 Expense도 함께 삭제할지 여부
        """
        try:
            # 관련 Expense 삭제 (옵션)
            if delete_expenses:
                expenses = await expense_service.get_expenses_by_receipt(receipt_id)
                for expense in expenses:
                    await expense_service.delete_expense(expense["id"])

            # Receipt 삭제
            self.db.collection(self.collection).document(receipt_id).delete()
            return True

        except Exception as e:
            raise Exception(f"영수증 삭제 실패: {str(e)}")


receipt_service = ReceiptService()
