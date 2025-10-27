from datetime import datetime
from typing import Optional


class Expense:
    """지출 내역 모델"""

    def __init__(
        self,
        id: str,
        user_id: str,
        receipt_id: str,
        category: str,  # 식비, 사무용품, 회식, 교통비, 기타 등
        amount: float,
        date: datetime,
        store_name: str,
        store_address: Optional[str] = None,
        store_phone_number: Optional[str] = None,
        description: Optional[str] = None,
        item_name: Optional[str] = None,
        classification_method: str = "auto",  # auto, manual
        classification_confidence: Optional[float] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.user_id = user_id
        self.receipt_id = receipt_id
        self.category = category
        self.amount = amount
        self.date = date
        self.store_name = store_name
        self.store_address = store_address
        self.store_phone_number = store_phone_number
        self.description = description
        self.item_name = item_name
        self.classification_method = classification_method
        self.classification_confidence = classification_confidence
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()

    def to_dict(self):
        """딕셔너리로 변환"""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "receipt_id": self.receipt_id,
            "category": self.category,
            "amount": self.amount,
            "date": self.date.isoformat(),
            "store_name": self.store_name,
            "store_address": self.store_address,
            "store_phone_number": self.store_phone_number,
            "description": self.description,
            "item_name": self.item_name,
            "classification_method": self.classification_method,
            "classification_confidence": self.classification_confidence,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }


# 카테고리 상수
class ExpenseCategory:
    """지출 카테고리 상수"""
    FOOD = "식비"
    OFFICE_SUPPLIES = "사무용품"
    DINING_OUT = "회식"
    TRANSPORTATION = "교통비"
    UTILITIES = "공과금"
    ENTERTAINMENT = "유흥"
    EDUCATION = "교육"
    HEALTH = "의료"
    OTHER = "기타"

    @classmethod
    def all_categories(cls):
        """모든 카테고리 반환"""
        return [
            cls.FOOD,
            cls.OFFICE_SUPPLIES,
            cls.DINING_OUT,
            cls.TRANSPORTATION,
            cls.UTILITIES,
            cls.ENTERTAINMENT,
            cls.EDUCATION,
            cls.HEALTH,
            cls.OTHER
        ]
