from typing import Dict, Tuple, Optional
import logging
from src.models.expense import ExpenseCategory

logger = logging.getLogger(__name__)


class CategoryService:
    """카테고리 자동 분류 서비스 (하이브리드: AI + 키워드)"""

    def __init__(self):
        # AI 모델 lazy import (선택적 의존성)
        self.ai_service = None
        try:
            from src.services.ai_category_service import ai_category_service
            self.ai_service = ai_category_service
            logger.info("AI classification service loaded")
        except ImportError:
            logger.warning("AI classification not available (dependencies missing)")
        except Exception as e:
            logger.warning(f"AI classification disabled: {e}")
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
                "도서", "book", "강의", "수강", "튜터",
                "교재", "영어교재", "토익", "토익강의", "토플", "영어", "중국어", "일본어",
                "강좌", "온라인강의", "인강"
            ],
            ExpenseCategory.HEALTH: [
                "병원", "hospital", "의원", "clinic",
                "약국", "pharmacy", "한의원", "치과"
            ]
        }

        # 품목명 기반 카테고리 매핑 (메인 분류 로직)
        self.item_keywords = {
            ExpenseCategory.FOOD: [
                # 음료
                "음료", "커피", "아메리카노", "라떼", "카페라떼", "카푸치노",
                "에스프레소", "주스", "차", "tea", "음료수", "cola", "콜라",
                # 식사/간식
                "음식", "식사", "간식", "과자", "빵", "케이크", "샌드위치",
                "김밥", "도시락", "햄버거", "피자", "치킨", "떡볶이",
                "라면", "국수", "우동", "파스타", "쌀", "밥"
            ],
            ExpenseCategory.DINING_OUT: [
                # 회식/술자리 관련
                "소주", "맥주", "와인", "양주", "사케", "위스키", "하이볼",
                "안주", "삼겹살", "목살", "갈비", "곱창", "대창", "막창",
                "고기", "육회", "회", "조개", "해산물", "구이", "찜",
                "전골", "탕", "찌개", "정식", "세트", "코스",
                # 고급 요리
                "스테이크", "랍스터", "오마카세"
            ],
            ExpenseCategory.OFFICE_SUPPLIES: [
                "볼펜", "샤프", "연필", "지우개", "공책", "노트", "수첩",
                "파일", "폴더", "바인더", "클립", "스테이플러", "호치키스",
                "테이프", "풀", "가위", "칼", "자", "형광펜", "마커",
                "포스트잇", "메모지", "용지", "A4", "복사지", "인쇄",
                "토너", "잉크", "프린터", "책상", "의자", "캐비닛"
            ],
            ExpenseCategory.TRANSPORTATION: [
                "휘발유", "경유", "lpg", "충전", "세차", "통행료",
                "택시", "버스", "지하철", "기차", "ktx", "주유"
            ],
            ExpenseCategory.UTILITIES: [
                "전기", "수도", "가스", "관리비", "요금"
            ],
            ExpenseCategory.HEALTH: [
                "약", "medicine", "처방", "진료", "검사", "치료"
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
                    return category, 0.7  # 중간 신뢰도 (유명 브랜드만 신뢰)

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
                    return category, 0.9  # 높은 신뢰도 (상품명이 더 정확)

        return ExpenseCategory.OTHER, 0.0

    def classify(
        self,
        store_name: str,
        item_name: Optional[str] = None,
        amount: Optional[float] = None
    ) -> Tuple[str, float]:
        """
        하이브리드 카테고리 분류 (AI + 키워드)

        분류 전략:
        1. AI 모델 분류 (신뢰도 0.8 이상)
        2. 키워드 매칭 - 품목명 우선 (신뢰도 0.9 이상)
        3. 키워드 매칭 - 상호명 (신뢰도 0.7 이상)
        4. AI 모델 낮은 신뢰도 결과
        5. 키워드 낮은 신뢰도 결과
        6. 기타

        Args:
            store_name: 상점명
            item_name: 품목명 (선택)
            amount: 금액 (선택, 추가 휴리스틱용)

        Returns:
            (카테고리, 신뢰도) 튜플
        """
        # === 1단계: AI 모델 분류 (Primary) ===
        if self.ai_service and self.ai_service.is_available():
            try:
                ai_category, ai_confidence = self.ai_service.classify(
                    store_name=store_name,
                    item_name=item_name
                )

                if ai_confidence >= 0.8:
                    logger.info(
                        f"AI classification (high confidence): "
                        f"{store_name}/{item_name} -> {ai_category} ({ai_confidence:.2f})"
                    )
                    return ai_category, ai_confidence

            except Exception as e:
                logger.error(f"AI classification error: {e}")

        # === 2단계: 키워드 품목명 분류 (높은 신뢰도) ===
        if item_name:
            item_category, item_confidence = self.classify_by_item(item_name)

            if item_confidence >= 0.9:
                logger.info(
                    f"Keyword classification (item): "
                    f"{item_name} -> {item_category} ({item_confidence:.2f})"
                )
                return item_category, item_confidence

        # === 3단계: 키워드 상호명 분류 (중간 신뢰도) ===
        store_category, store_confidence = self.classify_by_store(store_name)

        if store_confidence >= 0.7:
            logger.info(
                f"Keyword classification (store): "
                f"{store_name} -> {store_category} ({store_confidence:.2f})"
            )
            return store_category, store_confidence

        # === 4단계: AI 낮은 신뢰도 결과 사용 ===
        if self.ai_service and self.ai_service.is_available():
            try:
                ai_category, ai_confidence = self.ai_service.classify(
                    store_name=store_name,
                    item_name=item_name
                )

                if ai_confidence > 0.5:
                    logger.info(
                        f"AI classification (low confidence fallback): "
                        f"{store_name}/{item_name} -> {ai_category} ({ai_confidence:.2f})"
                    )
                    return ai_category, ai_confidence

            except Exception as e:
                logger.error(f"AI classification error (fallback): {e}")

        # === 5단계: 키워드 낮은 신뢰도 결과 ===
        if item_name:
            item_category, item_confidence = self.classify_by_item(item_name)
            if item_confidence > 0:
                logger.info(
                    f"Keyword classification (item fallback): "
                    f"{item_name} -> {item_category} ({item_confidence:.2f})"
                )
                return item_category, item_confidence

        if store_confidence > 0:
            logger.info(
                f"Keyword classification (store fallback): "
                f"{store_name} -> {store_category} ({store_confidence:.2f})"
            )
            return store_category, store_confidence

        # === 6단계: 금액 기반 휴리스틱 (선택적) ===
        if amount and amount > 100000:  # 10만원 이상
            # 대형 지출은 회식이나 사무용품일 가능성
            logger.info(f"Amount-based heuristic: large expense -> DINING_OUT")
            return ExpenseCategory.DINING_OUT, 0.3

        # === 7단계: 기본값 ===
        logger.warning(
            f"Classification failed for {store_name}/{item_name} -> OTHER"
        )
        return ExpenseCategory.OTHER, 0.0

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
