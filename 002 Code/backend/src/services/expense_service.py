from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from src.core.firebase import firebase_client
from src.services.category_service import category_service


class ExpenseService:
    """지출 내역 관리 서비스"""

    def __init__(self):
        self.db = firebase_client.db
        self.collection = "expenses"

    async def create_expense(
        self,
        user_id: str,
        receipt_id: str,
        store_name: str,
        amount: float,
        date: datetime,
        store_address: str = None,
        store_phone_number: str = None,
        item_name: str = None,
        category: str = None,
        description: str = None,
        budget_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        지출 내역 생성 (카테고리 자동 분류)

        Args:
            user_id: 사용자 ID
            receipt_id: 영수증 ID
            store_name: 상점명
            amount: 금액
            date: 날짜
            item_name: 품목명 (선택)
            category: 카테고리 (수동 지정 시)
            description: 설명 (선택)

        Returns:
            생성된 지출 내역
        """
        try:
            # 카테고리가 지정되지 않은 경우 자동 분류
            if not category:
                category, confidence = category_service.classify(
                    store_name=store_name,
                    item_name=item_name,
                    amount=amount
                )
                classification_method = "auto"
            else:
                confidence = 1.0
                classification_method = "manual"

            # Firestore에 저장할 데이터
            expense_data = {
                "user_id": user_id,
                "receipt_id": receipt_id,
                "category": category,
                "amount": amount,
                "date": date,
                "store_name": store_name,
                "store_address": store_address or "",
                "store_phone_number": store_phone_number or "",
                "description": description,
                "item_name": item_name,
                "classification_method": classification_method,
                "classification_confidence": confidence,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }
            
            # budget_id 추가 (있는 경우)
            if budget_id:
                expense_data["budget_id"] = budget_id

            # Firestore에 저장
            doc_ref = self.db.collection(self.collection).document()
            doc_ref.set(expense_data)

            expense_data["id"] = doc_ref.id
            return expense_data

        except Exception as e:
            raise Exception(f"지출 내역 생성 실패: {str(e)}")

    async def get_expenses(
        self,
        user_id: str,
        category: str = None,
        start_date: datetime = None,
        end_date: datetime = None,
        limit: int = 100,
        organizationName: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        지출 내역 목록 조회

        Args:
            user_id: 사용자 ID
            category: 카테고리 필터 (선택)
            start_date: 시작 날짜 (선택)
            end_date: 종료 날짜 (선택)
            limit: 최대 결과 수
            organizationName: 조직 이름 (있는 경우 조직 멤버 전체 지출 조회)

        Returns:
            지출 내역 리스트
        """
        try:
            # 조직 공유 조회인 경우
            if organizationName:
                # 같은 조직의 모든 사용자 ID 가져오기
                users_ref = self.db.collection("users")\
                    .where("organizationName", "==", organizationName)\
                    .stream()
                
                user_ids = []
                for user_doc in users_ref:
                    user_ids.append(user_doc.id)
                
                # 모든 사용자의 지출 조회
                docs_list = []
                for org_user_id in user_ids:
                    query = self.db.collection(self.collection).where("user_id", "==", org_user_id)
                    docs = query.stream()
                    docs_list.extend(docs)
                
                expenses = []
                for doc in docs_list:
                    expense_data = doc.to_dict()
                    expense_data["id"] = doc.id

                    # Python에서 필터링
                    if category and expense_data.get("category") != category:
                        continue
                    if start_date and expense_data.get("date") and expense_data["date"] < start_date:
                        continue
                    if end_date and expense_data.get("date") and expense_data["date"] > end_date:
                        continue

                    expenses.append(expense_data)
            else:
                # 개인 지출만 조회
                query = self.db.collection(self.collection).where("user_id", "==", user_id)
                docs = query.stream()
                expenses = []
                for doc in docs:
                    expense_data = doc.to_dict()
                    expense_data["id"] = doc.id

                    # Python에서 필터링
                    if category and expense_data.get("category") != category:
                        continue
                    if start_date and expense_data.get("date") and expense_data["date"] < start_date:
                        continue
                    if end_date and expense_data.get("date") and expense_data["date"] > end_date:
                        continue

                    expenses.append(expense_data)

            # Python에서 정렬 (날짜 기준 내림차순)
            expenses.sort(key=lambda x: x.get("date", datetime.min), reverse=True)

            # limit 적용
            return expenses[:limit]

        except Exception as e:
            raise Exception(f"지출 목록 조회 실패: {str(e)}")

    async def get_expense(self, expense_id: str) -> Optional[Dict[str, Any]]:
        """특정 지출 내역 조회"""
        try:
            doc = self.db.collection(self.collection).document(expense_id).get()

            if doc.exists:
                expense_data = doc.to_dict()
                expense_data["id"] = doc.id
                return expense_data
            return None

        except Exception as e:
            raise Exception(f"지출 조회 실패: {str(e)}")

    async def update_expense(
        self,
        expense_id: str,
        update_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        지출 내역 수정

        Args:
            expense_id: 지출 ID
            update_data: 수정할 데이터

        Returns:
            수정된 지출 내역
        """
        try:
            update_data["updated_at"] = datetime.utcnow()

            # 카테고리가 수동으로 변경된 경우
            if "category" in update_data:
                update_data["classification_method"] = "manual"
                update_data["classification_confidence"] = 1.0

            doc_ref = self.db.collection(self.collection).document(expense_id)
            doc_ref.update(update_data)

            # 수정된 데이터 반환
            updated_doc = doc_ref.get()
            expense_data = updated_doc.to_dict()
            expense_data["id"] = updated_doc.id
            return expense_data

        except Exception as e:
            raise Exception(f"지출 수정 실패: {str(e)}")

    async def delete_expense(self, expense_id: str) -> bool:
        """지출 내역 삭제"""
        try:
            self.db.collection(self.collection).document(expense_id).delete()
            return True
        except Exception as e:
            raise Exception(f"지출 삭제 실패: {str(e)}")

    async def get_statistics(
        self,
        user_id: str,
        start_date: datetime = None,
        end_date: datetime = None,
        organizationName: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        지출 통계 조회 (재무제표용)

        Args:
            user_id: 사용자 ID
            start_date: 시작 날짜 (기본: 이번 달 1일)
            end_date: 종료 날짜 (기본: 오늘)
            organizationName: 조직 이름 (있는 경우 조직 멤버 전체 지출 통계)

        Returns:
            카테고리별 통계 및 전체 요약
        """
        try:
            # 기본값 설정
            if not end_date:
                end_date = datetime.utcnow()
            if not start_date:
                start_date = datetime(end_date.year, end_date.month, 1)

            # 해당 기간의 모든 지출 조회
            expenses = await self.get_expenses(
                user_id=user_id,
                start_date=start_date,
                end_date=end_date,
                limit=10000,
                organizationName=organizationName
            )

            # 카테고리별 집계
            category_stats = {}
            total_amount = 0.0
            total_count = len(expenses)

            for expense in expenses:
                category = expense.get("category", "기타")
                amount = expense.get("amount", 0.0)

                if category not in category_stats:
                    category_stats[category] = {
                        "category": category,
                        "total_amount": 0.0,
                        "count": 0
                    }

                category_stats[category]["total_amount"] += amount
                category_stats[category]["count"] += 1
                total_amount += amount

            # 퍼센트 계산
            by_category = []
            for category, stats in category_stats.items():
                stats["percentage"] = (stats["total_amount"] / total_amount * 100) if total_amount > 0 else 0
                by_category.append(stats)

            # 금액 기준 내림차순 정렬
            by_category.sort(key=lambda x: x["total_amount"], reverse=True)

            return {
                "total_amount": total_amount,
                "total_count": total_count,
                "by_category": by_category,
                "start_date": start_date,
                "end_date": end_date
            }

        except Exception as e:
            raise Exception(f"통계 조회 실패: {str(e)}")

    async def get_expenses_by_receipt(
        self,
        receipt_id: str
    ) -> List[Dict[str, Any]]:
        """영수증 ID로 지출 내역 조회"""
        try:
            query = self.db.collection(self.collection).where("receipt_id", "==", receipt_id)
            docs = query.stream()

            expenses = []
            for doc in docs:
                expense_data = doc.to_dict()
                expense_data["id"] = doc.id
                expenses.append(expense_data)

            return expenses

        except Exception as e:
            raise Exception(f"영수증별 지출 조회 실패: {str(e)}")


expense_service = ExpenseService()
