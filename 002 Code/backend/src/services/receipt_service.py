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
            # 1. 이미지를 Firebase Storage에 업로드
            uploaded_image_url = None
            if image_data:
                uploaded_image_url = firebase_client.upload_image(
                    image_data=image_data,
                    user_id=user_id
                )
                if uploaded_image_url:
                    print(f"[Storage] 이미지 업로드 완료: {uploaded_image_url}")
                    image_url = uploaded_image_url

            # 2. OCR 처리
            print(f"[OCR] Receipt OCR processing started...")
            ocr_result = await ocr_service.process_receipt(image_data=image_data)

            if ocr_result["status"] != "success":
                raise Exception(f"OCR 처리 실패: {ocr_result.get('message', 'Unknown error')}")

            ocr_data = ocr_result["data"]

            # 2. Receipt 데이터 생성
            # OCR 데이터에서 날짜 처리
            if isinstance(ocr_data["date"], datetime):
                purchase_date = ocr_data["date"]
            else:
                purchase_date = datetime.strptime(ocr_data["date"], "%Y-%m-%d")

            receipt_data = {
                "user_id": user_id,
                "store_name": ocr_data["store_name"],
                "store_address": ocr_data.get("store_address", ""),
                "store_phone_number": ocr_data.get("store_phone_number", ""),
                "total_amount": ocr_data["total_amount"],
                "purchase_date": purchase_date,
                "items": [],  # 개별 품목은 저장하지 않음
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

            print(f"[SUCCESS] Receipt saved: {receipt_ref.id}")

            # 4. 총액으로 단일 Expense 자동 생성
            created_expenses = []

            # 카테고리 자동 분류
            category, confidence = category_service.classify(
                store_name=ocr_data["store_name"],
                item_name="",
                amount=ocr_data["total_amount"]
            )

            # Expense 생성
            expense = await expense_service.create_expense(
                user_id=user_id,
                receipt_id=receipt_ref.id,
                store_name=ocr_data["store_name"],
                store_address=ocr_data.get("store_address", ""),
                store_phone_number=ocr_data.get("store_phone_number", ""),
                amount=ocr_data["total_amount"],
                date=receipt_data["purchase_date"],
                item_name="",
                category=category,
                description=f"{ocr_data['store_name']}에서 구매"
            )

            created_expenses.append(expense)
            print(f"[EXPENSE] Created: {category} - {ocr_data['total_amount']} KRW")

            return {
                "status": "success",
                "receipt": receipt_data,
                "expenses": created_expenses,
                "message": f"영수증 처리 완료: 총 {ocr_data['total_amount']}원의 지출 내역이 생성되었습니다"
            }

        except Exception as e:
            # 에러 발생 시 Receipt는 failed 상태로 저장
            error_receipt_data = {
                "user_id": user_id,
                "store_name": "",
                "store_address": "",
                "store_phone_number": "",
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

    async def find_matching_receipt(
        self,
        user_id: str,
        store_name: str,
        amount: float,
        date: datetime,
        tolerance_days: int = 1,
        amount_tolerance_percent: float = 5.0
    ) -> Optional[Dict[str, Any]]:
        """
        지출 내역과 매칭되는 영수증 찾기

        Args:
            user_id: 사용자 ID
            store_name: 상호명
            amount: 금액
            date: 날짜
            tolerance_days: 날짜 허용 오차 (일)
            amount_tolerance_percent: 금액 허용 오차 (%)

        Returns:
            매칭되는 영수증 또는 None
        """
        try:
            print(f"[Receipt Match] 영수증 매칭 시도 - user: {user_id}, store: {store_name}, amount: {amount}, date: {date}")

            # user_id로 필터링
            receipts_ref = self.db.collection(self.collection).where("user_id", "==", user_id)
            receipts = receipts_ref.stream()

            # 날짜 범위 계산
            from datetime import timedelta
            date_min = date - timedelta(days=tolerance_days)
            date_max = date + timedelta(days=tolerance_days)

            # 금액 범위 계산
            amount_min = amount * (1 - amount_tolerance_percent / 100)
            amount_max = amount * (1 + amount_tolerance_percent / 100)

            best_match = None
            best_score = 0

            for receipt_doc in receipts:
                receipt_data = receipt_doc.to_dict()
                receipt_data["id"] = receipt_doc.id

                # image_url이 없는 receipt는 스킵
                if not receipt_data.get("image_url"):
                    continue

                # 매칭 점수 계산
                score = 0

                # 1. 상호명 매칭 (50점)
                receipt_store = receipt_data.get("store_name", "")
                if receipt_store and store_name:
                    if receipt_store.lower() == store_name.lower():
                        score += 50
                    elif receipt_store.lower() in store_name.lower() or store_name.lower() in receipt_store.lower():
                        score += 30

                # 2. 금액 매칭 (30점)
                receipt_amount = receipt_data.get("total_amount", 0)
                if amount_min <= receipt_amount <= amount_max:
                    # 금액이 정확할수록 높은 점수
                    amount_diff_percent = abs(receipt_amount - amount) / amount * 100 if amount > 0 else 100
                    amount_score = max(0, 30 - amount_diff_percent)
                    score += amount_score
                    print(f"[Receipt Match] 금액 매칭: receipt={receipt_amount}, expense={amount}, diff={amount_diff_percent:.2f}%, score={amount_score}")

                # 3. 날짜 매칭 (20점)
                receipt_date = receipt_data.get("purchase_date")
                # 날짜 타입 변환
                if receipt_date and not isinstance(receipt_date, datetime):
                    try:
                        if isinstance(receipt_date, str):
                            receipt_date = datetime.fromisoformat(receipt_date.replace('Z', '+00:00'))
                    except:
                        receipt_date = None

                if receipt_date and isinstance(receipt_date, datetime):
                    if date_min <= receipt_date <= date_max:
                        # 날짜가 정확할수록 높은 점수
                        days_diff = abs((receipt_date - date).days)
                        date_score = max(0, 20 - days_diff * 5)
                        score += date_score
                        print(f"[Receipt Match] 날짜 매칭: receipt={receipt_date}, expense={date}, diff={days_diff}일, score={date_score}")

                print(f"[Receipt Match] Receipt {receipt_doc.id}: total_score={score}, store={receipt_store}, amount={receipt_amount}")

                # 최고 점수 업데이트 (최소 50점 이상으로 완화)
                if score > best_score and score >= 50:
                    best_score = score
                    best_match = receipt_data

            if best_match:
                print(f"[Receipt Match] 매칭 성공! Receipt ID: {best_match['id']}, score: {best_score}")
                return best_match
            else:
                print(f"[Receipt Match] 매칭 실패 - 적합한 영수증을 찾지 못함")
                return None

        except Exception as e:
            print(f"[Receipt Match] 에러: {str(e)}")
            return None


receipt_service = ReceiptService()
