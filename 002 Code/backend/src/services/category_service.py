from typing import Dict, Tuple
from src.models.expense import ExpenseCategory


class CategoryService:
    """카테고리 자동 분류 서비스"""

    def __init__(self):
        # 상호명 기반 카테고리 매핑
        self.store_keywords = {
            ExpenseCategory.FOOD: [
                "스타벅스", "커피", "카페", "cafe", "coffee",
                "맥도날드", "버거킹", "롯데리아", "kfc",
                "편의점", "gs25", "cu", "세븐일레븐", "이마트24",
                "김밥", "치킨", "피자", "중국집", "한식", "일식", "양식",
                "베이커리", "빵", "마트", "마켓", "슈퍼"
            ],
            ExpenseCategory.OFFICE_SUPPLIES: [
                "다이소", "알파", "문구", "사무", "office",
                "복사", "인쇄", "프린트", "용지", "펜", "노트",
                "모닝글로리", "교보문고", "yes24"
            ],
            ExpenseCategory.DINING_OUT: [
                "술집", "bar", "pub", "호프", "포차",
                "삼겹살", "고깃집", "회식", "연회", "뷔페",
                "레스토랑", "restaurant"
            ],
            ExpenseCategory.TRANSPORTATION: [
                "택시", "taxi", "우버", "카카오택시",
                "주차", "parking", "주유", "gas", "oil",
                "버스", "지하철", "ktx", "기차", "렌터카"
            ],
            ExpenseCategory.UTILITIES: [
                "전기", "수도", "가스", "관리비",
                "통신", "인터넷", "kt", "skt", "lg", "u+"
            ],
            ExpenseCategory.ENTERTAINMENT: [
                "cgv", "메가박스", "롯데시네마", "영화",
                "노래방", "pc방", "오락", "게임"
            ],
            ExpenseCategory.EDUCATION: [
                "학원", "교육", "education", "academy",
                "도서", "book", "강의", "수강", "튜터"
            ],
            ExpenseCategory.HEALTH: [
                "병원", "hospital", "의원", "clinic",
                "약국", "pharmacy", "한의원", "치과"
            ]
        }

        # 품목명 기반 카테고리 매핑
        self.item_keywords = {
            ExpenseCategory.FOOD: [
                "음료", "커피", "음식", "식사", "간식", "과자",
                "아메리카노", "라떼", "주스", "빵", "케이크"
            ],
            ExpenseCategory.OFFICE_SUPPLIES: [
                "볼펜", "공책", "노트", "파일", "폴더",
                "클립", "스테이플러", "테이프", "풀", "가위"
            ],
            ExpenseCategory.DINING_OUT: [
                "소주", "맥주", "와인", "양주", "안주",
                "삼겹살", "곱창", "회", "조개"
            ],
            ExpenseCategory.TRANSPORTATION: [
                "휘발유", "경유", "충전", "세차", "통행료"
            ]
        }

    def classify_by_store(self, store_name: str) -> Tuple[str, float]:
        """
        상호명 기반 카테고리 분류

        Args:
            store_name: 상점명

        Returns:
            (카테고리, 신뢰도) 튜플
        """
        if not store_name:
            return ExpenseCategory.OTHER, 0.0

        store_name_lower = store_name.lower()

        for category, keywords in self.store_keywords.items():
            for keyword in keywords:
                if keyword.lower() in store_name_lower:
                    return category, 0.9  # 높은 신뢰도

        return ExpenseCategory.OTHER, 0.0

    def classify_by_item(self, item_name: str) -> Tuple[str, float]:
        """
        품목명 기반 카테고리 분류

        Args:
            item_name: 품목명

        Returns:
            (카테고리, 신뢰도) 튜플
        """
        if not item_name:
            return ExpenseCategory.OTHER, 0.0

        item_name_lower = item_name.lower()

        for category, keywords in self.item_keywords.items():
            for keyword in keywords:
                if keyword.lower() in item_name_lower:
                    return category, 0.7  # 중간 신뢰도

        return ExpenseCategory.OTHER, 0.0

    def classify(
        self,
        store_name: str,
        item_name: str = None,
        amount: float = None
    ) -> Tuple[str, float]:
        """
        종합 카테고리 분류

        Args:
            store_name: 상점명
            item_name: 품목명 (선택)
            amount: 금액 (선택, 추가 휴리스틱용)

        Returns:
            (카테고리, 신뢰도) 튜플
        """
        # 1. 상호명 기반 분류 (우선순위 높음)
        store_category, store_confidence = self.classify_by_store(store_name)

        if store_confidence >= 0.9:
            return store_category, store_confidence

        # 2. 품목명 기반 분류
        if item_name:
            item_category, item_confidence = self.classify_by_item(item_name)

            if item_confidence >= 0.7:
                return item_category, item_confidence

        # 3. 금액 기반 휴리스틱 (선택적)
        if amount and amount > 100000:  # 10만원 이상
            # 대형 지출은 회식이나 사무용품일 가능성
            if store_confidence > 0:
                return store_category, store_confidence * 0.8

        # 4. 기본값
        return store_category if store_category != ExpenseCategory.OTHER else ExpenseCategory.OTHER, store_confidence

    def get_category_suggestions(self, text: str) -> list[Dict[str, any]]:
        """
        텍스트 기반 카테고리 제안

        Args:
            text: 검색 텍스트

        Returns:
            제안 카테고리 리스트
        """
        suggestions = []
        text_lower = text.lower()

        for category, keywords in self.store_keywords.items():
            matches = [kw for kw in keywords if text_lower in kw.lower() or kw.lower() in text_lower]
            if matches:
                suggestions.append({
                    "category": category,
                    "matched_keywords": matches[:3],
                    "confidence": 0.8
                })

        return suggestions


category_service = CategoryService()
