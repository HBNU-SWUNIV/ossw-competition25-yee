"""
AI 기반 카테고리 분류 서비스
License: Apache 2.0 (polyglot-ko model)
"""
from typing import Tuple, Optional
import logging
from transformers import pipeline
from src.models.expense import ExpenseCategory

logger = logging.getLogger(__name__)


class AICategoryService:
    """
    Zero-shot Classification을 활용한 AI 기반 카테고리 분류

    모델: MoritzLaurer/mDeBERTa-v3-base-xnli-multilingual-nli-2mil7
    라이선스: MIT License (상업적 사용 가능)
    """

    def __init__(self):
        self.classifier = None
        self.categories = [
            ExpenseCategory.FOOD,
            ExpenseCategory.DINING_OUT,
            ExpenseCategory.OFFICE_SUPPLIES,
            ExpenseCategory.TRANSPORTATION,
            ExpenseCategory.UTILITIES,
            ExpenseCategory.HEALTH,
            ExpenseCategory.ENTERTAINMENT,
            ExpenseCategory.EDUCATION,
            ExpenseCategory.OTHER
        ]

        # 카테고리별 설명 (AI가 더 잘 이해하도록)
        self.category_descriptions = {
            ExpenseCategory.FOOD: "식사, 간식, 커피, 음료, 도시락, 빵, 과자",
            ExpenseCategory.DINING_OUT: "회식, 술, 안주, 고기, 회, 저녁모임, 소주, 맥주",
            ExpenseCategory.OFFICE_SUPPLIES: "사무용품, 문구류, 볼펜, 노트, 프린터, 책상, 의자",
            ExpenseCategory.TRANSPORTATION: "교통비, 주유, 택시, 버스, 지하철, 통행료",
            ExpenseCategory.UTILITIES: "공과금, 전기, 수도, 가스, 통신요금",
            ExpenseCategory.HEALTH: "병원, 약국, 진료, 치료, 의약품",
            ExpenseCategory.ENTERTAINMENT: "오락, 영화, 공연, 게임, 노래방",
            ExpenseCategory.EDUCATION: "교육, 학원, 강의, 교재, 수강료",
            ExpenseCategory.OTHER: "기타 항목"
        }

        self._initialize_model()

    def _initialize_model(self):
        """
        AI 모델 초기화 (lazy loading)
        """
        try:
            logger.info("Initializing AI classification model...")

            # Zero-shot classification pipeline
            # 다국어 지원 모델 (한국어 포함)
            self.classifier = pipeline(
                "zero-shot-classification",
                model="MoritzLaurer/mDeBERTa-v3-base-xnli-multilingual-nli-2mil7",
                device=-1  # CPU 사용 (GPU 없어도 동작)
            )

            logger.info("AI model initialized successfully")

        except Exception as e:
            logger.error(f"Failed to initialize AI model: {e}")
            logger.warning("AI classification will be disabled")
            self.classifier = None

    def classify(
        self,
        store_name: str,
        item_name: Optional[str] = None
    ) -> Tuple[str, float]:
        """
        AI 기반 카테고리 분류

        Args:
            store_name: 상점명
            item_name: 품목명 (선택)

        Returns:
            (카테고리, 신뢰도) 튜플
        """
        if not self.classifier:
            return ExpenseCategory.OTHER, 0.0

        try:
            # 분류할 텍스트 구성
            text = self._build_classification_text(store_name, item_name)

            # Zero-shot classification 수행
            result = self.classifier(
                text,
                candidate_labels=list(self.category_descriptions.values()),
                hypothesis_template="이 영수증 항목은 {}에 해당합니다."
            )

            # 결과 파싱
            best_label = result['labels'][0]
            best_score = result['scores'][0]

            # 설명에서 카테고리 코드로 역매핑
            category = self._description_to_category(best_label)

            logger.info(
                f"AI Classification: '{text}' -> {category} "
                f"(confidence: {best_score:.2f})"
            )

            return category, best_score

        except Exception as e:
            logger.error(f"AI classification failed: {e}")
            return ExpenseCategory.OTHER, 0.0

    def _build_classification_text(
        self,
        store_name: str,
        item_name: Optional[str]
    ) -> str:
        """
        분류용 텍스트 구성
        """
        if item_name:
            return f"{store_name}에서 {item_name}"
        else:
            return f"{store_name}"

    def _description_to_category(self, description: str) -> str:
        """
        카테고리 설명을 카테고리 코드로 변환
        """
        for category, desc in self.category_descriptions.items():
            if desc == description:
                return category

        return ExpenseCategory.OTHER

    def is_available(self) -> bool:
        """
        AI 모델 사용 가능 여부 확인
        """
        return self.classifier is not None


# 싱글톤 인스턴스
ai_category_service = AICategoryService()
