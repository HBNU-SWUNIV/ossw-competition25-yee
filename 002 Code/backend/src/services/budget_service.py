from typing import List, Dict, Any, Optional
from datetime import datetime
from src.core.firebase import firebase_client


class BudgetService:
    """예산 관리 서비스"""

    def __init__(self):
        self.db = firebase_client.db
        self.collection = "budgets"
        self.expense_collection = "expenses"

    async def get_all_budgets(self, user_id: str, organizationName: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        사용자의 모든 예산 조회

        Args:
            user_id: 사용자 ID
            organizationName: 조직 이름 (조직별 예산 조회용)

        Returns:
            예산 목록 (spent, remaining 포함)
        """
        try:
            budgets: List[Dict[str, Any]] = []

            # 1) 개인 예산 조회
            user_budgets_ref = self.db.collection(self.collection)\
                .where("user_id", "==", user_id)\
                .stream()

            for doc in user_budgets_ref:
                budget_data = doc.to_dict()
                budget_data["id"] = doc.id

                spent = await self._calculate_spent(
                    user_id,
                    budget_data.get("id"),  # budget_id
                    budget_data.get("category"),
                    budget_data.get("organizationName")
                )
                budget_data["spent"] = spent
                budget_data["remaining"] = budget_data["amount"] - spent
                budgets.append(budget_data)

            # 2) 조직 예산 추가 조회 (조직 이름이 있는 경우)
            if organizationName:
                org_budgets_ref = self.db.collection(self.collection)\
                    .where("organizationName", "==", organizationName)\
                    .stream()

                # 중복 방지를 위한 ID 집합
                existing_ids = {b["id"] for b in budgets}

                for doc in org_budgets_ref:
                    if doc.id in existing_ids:
                        continue
                    budget_data = doc.to_dict()
                    budget_data["id"] = doc.id

                    spent = await self._calculate_spent(
                        user_id,
                        budget_data.get("id"),  # budget_id
                        budget_data.get("category"),
                        budget_data.get("organizationName") or organizationName
                    )
                    budget_data["spent"] = spent
                    budget_data["remaining"] = budget_data["amount"] - spent
                    budgets.append(budget_data)

            return budgets

        except Exception as e:
            raise Exception(f"예산 목록 조회 실패: {str(e)}")

    async def get_budget(self, budget_id: str, user_id: str) -> Optional[Dict[str, Any]]:
        """
        특정 예산 조회

        Args:
            budget_id: 예산 ID
            user_id: 사용자 ID (권한 확인용)

        Returns:
            예산 정보 (spent, remaining 포함)
        """
        try:
            # Firestore에서 예산 조회
            doc_ref = self.db.collection(self.collection).document(budget_id)
            doc = doc_ref.get()

            if not doc.exists:
                return None

            budget_data = doc.to_dict()
            budget_data["id"] = doc.id

            # 권한 확인 (본인 예산만 조회 가능)
            if budget_data.get("user_id") != user_id:
                raise Exception("권한이 없습니다")

            # 실제 지출 금액 계산
            spent = await self._calculate_spent(user_id, budget_id, budget_data.get("category"))
            budget_data["spent"] = spent
            budget_data["remaining"] = budget_data["amount"] - spent

            return budget_data

        except Exception as e:
            raise Exception(f"예산 조회 실패: {str(e)}")

    async def create_budget(self, user_id: str, budget_data: Dict[str, Any], organizationName: Optional[str] = None) -> Dict[str, Any]:
        """
        예산 생성

        Args:
            user_id: 사용자 ID
            budget_data: 예산 데이터 (name, amount, category, organizationName)
            organizationName: 조직 이름 (옵션)

        Returns:
            생성된 예산 정보
        """
        try:
            # Firestore에 저장할 데이터
            new_budget = {
                "user_id": user_id,
                "name": budget_data["name"],
                "amount": budget_data["amount"],
                "category": budget_data.get("category", "전체"),
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }
            
            # 조직 이름 추가 (있는 경우)
            org_name = budget_data.get("organizationName") or organizationName
            if org_name:
                new_budget["organizationName"] = org_name

            # Firestore에 저장
            doc_ref = self.db.collection(self.collection).document()
            doc_ref.set(new_budget)

            # 응답 데이터 생성
            new_budget["id"] = doc_ref.id
            new_budget["spent"] = 0.0
            new_budget["remaining"] = new_budget["amount"]

            return new_budget

        except Exception as e:
            raise Exception(f"예산 생성 실패: {str(e)}")

    async def migrate_budgets_to_organization(self, user_id: str, organizationName: str) -> int:
        """
        기존 개인 예산을 조직 예산으로 변환 (organizationName 설정)

        Returns:
            업데이트된 예산 문서 수
        """
        try:
            updated = 0
            budgets_ref = self.db.collection(self.collection)\
                .where("user_id", "==", user_id)\
                .stream()

            for doc in budgets_ref:
                data = doc.to_dict()
                # 이미 조직 예산이면 스킵
                if data.get("organizationName"):
                    continue
                # 조직 이름 설정
                self.db.collection(self.collection).document(doc.id).update({
                    "organizationName": organizationName,
                    "updated_at": datetime.utcnow()
                })
                updated += 1

            return updated
        except Exception as e:
            raise Exception(f"예산 조직 마이그레이션 실패: {str(e)}")

    async def update_budget(
        self,
        budget_id: str,
        user_id: str,
        budget_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        예산 수정

        Args:
            budget_id: 예산 ID
            user_id: 사용자 ID (권한 확인용)
            budget_data: 수정할 데이터

        Returns:
            수정된 예산 정보
        """
        try:
            # 기존 예산 조회 및 권한 확인
            doc_ref = self.db.collection(self.collection).document(budget_id)
            doc = doc_ref.get()

            if not doc.exists:
                raise Exception("예산을 찾을 수 없습니다")

            existing_budget = doc.to_dict()
            if existing_budget.get("user_id") != user_id:
                raise Exception("권한이 없습니다")

            # 수정 가능한 필드만 업데이트
            update_data = {
                "updated_at": datetime.utcnow()
            }

            if "name" in budget_data:
                update_data["name"] = budget_data["name"]
            if "amount" in budget_data:
                update_data["amount"] = budget_data["amount"]
            if "category" in budget_data:
                update_data["category"] = budget_data["category"]

            # Firestore 업데이트
            doc_ref.update(update_data)

            # 업데이트된 데이터 반환
            existing_budget.update(update_data)
            existing_budget["id"] = budget_id

            # 실제 지출 금액 계산
            spent = await self._calculate_spent(user_id, budget_id, existing_budget.get("category"))
            existing_budget["spent"] = spent
            existing_budget["remaining"] = existing_budget["amount"] - spent

            return existing_budget

        except Exception as e:
            raise Exception(f"예산 수정 실패: {str(e)}")

    async def delete_budget(self, budget_id: str, user_id: str, organizationName: Optional[str] = None) -> bool:
        """
        예산 삭제

        Args:
            budget_id: 예산 ID
            user_id: 사용자 ID (권한 확인용)

        Returns:
            삭제 성공 여부
        """
        try:
            # 기존 예산 조회 및 권한 확인
            doc_ref = self.db.collection(self.collection).document(budget_id)
            doc = doc_ref.get()

            if not doc.exists:
                raise Exception("예산을 찾을 수 없습니다")

            existing_budget = doc.to_dict()
            # 권한 확인: 예산 소유자이거나 같은 조직 예산이면 삭제 허용
            if existing_budget.get("user_id") != user_id:
                budget_org = existing_budget.get("organizationName")
                if not (budget_org and organizationName and budget_org == organizationName):
                    raise Exception("권한이 없습니다")

            # Firestore에서 삭제
            doc_ref.delete()

            return True

        except Exception as e:
            raise Exception(f"예산 삭제 실패: {str(e)}")

    async def _calculate_spent(self, user_id: str, budget_id: Optional[str] = None, category: Optional[str] = None, organizationName: Optional[str] = None) -> float:
        """
        예산별 지출 금액 계산 (budget_id 우선, 없으면 category 기반)

        Args:
            user_id: 사용자 ID
            budget_id: 예산 ID (우선 사용)
            category: 카테고리 (budget_id가 없을 때 fallback)
            organizationName: 조직 이름 (있는 경우 조직 멤버 전체 지출 합산)

        Returns:
            총 지출 금액
        """
        try:
            # budget_id가 있으면 해당 예산에 연결된 지출만 계산
            if budget_id:
                # 조직 공유 예산인 경우
                if organizationName:
                    # 같은 조직의 모든 사용자 ID 가져오기
                    users_ref = self.db.collection("users")\
                        .where("organizationName", "==", organizationName)\
                        .stream()
                    
                    user_ids = []
                    for user_doc in users_ref:
                        user_ids.append(user_doc.id)
                    
                    # 모든 사용자의 해당 예산 지출 합산
                    total_spent = 0.0
                    for org_user_id in user_ids:
                        expenses_ref = self.db.collection(self.expense_collection)\
                            .where("user_id", "==", org_user_id)\
                            .where("budget_id", "==", budget_id)
                        
                        expenses = expenses_ref.stream()
                        
                        for expense_doc in expenses:
                            expense_data = expense_doc.to_dict()
                            total_spent += expense_data.get("amount", 0.0)
                    
                    return total_spent
                else:
                    # 개인 예산인 경우
                    expenses_ref = self.db.collection(self.expense_collection)\
                        .where("user_id", "==", user_id)\
                        .where("budget_id", "==", budget_id)

                    expenses = expenses_ref.stream()

                    # 총 지출 금액 계산
                    total_spent = 0.0
                    for expense_doc in expenses:
                        expense_data = expense_doc.to_dict()
                        total_spent += expense_data.get("amount", 0.0)

                    return total_spent
            
            # budget_id가 없으면 기존 category 기반 로직 (하위 호환)
            # 조직 공유 예산인 경우
            if organizationName:
                # 같은 조직의 모든 사용자 ID 가져오기
                users_ref = self.db.collection("users")\
                    .where("organizationName", "==", organizationName)\
                    .stream()
                
                user_ids = []
                for user_doc in users_ref:
                    user_ids.append(user_doc.id)
                
                # 모든 사용자의 지출 합산
                total_spent = 0.0
                for org_user_id in user_ids:
                    expenses_ref = self.db.collection(self.expense_collection)\
                        .where("user_id", "==", org_user_id)
                    
                    # 카테고리 필터 (있는 경우)
                    if category and category != "전체":
                        expenses_ref = expenses_ref.where("category", "==", category)
                    
                    expenses = expenses_ref.stream()
                    
                    for expense_doc in expenses:
                        expense_data = expense_doc.to_dict()
                        total_spent += expense_data.get("amount", 0.0)
                
                return total_spent
            else:
                # 개인 예산인 경우
                expenses_ref = self.db.collection(self.expense_collection)\
                    .where("user_id", "==", user_id)

                # 카테고리 필터 (있는 경우)
                if category and category != "전체":
                    expenses_ref = expenses_ref.where("category", "==", category)

                expenses = expenses_ref.stream()

                # 총 지출 금액 계산
                total_spent = 0.0
                for expense_doc in expenses:
                    expense_data = expense_doc.to_dict()
                    total_spent += expense_data.get("amount", 0.0)

                return total_spent

        except Exception as e:
            # 에러가 나도 0 반환 (지출 계산 실패해도 예산 조회는 가능하게)
            print(f"지출 계산 실패: {str(e)}")
            return 0.0


budget_service = BudgetService()
