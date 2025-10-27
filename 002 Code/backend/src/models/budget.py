from datetime import datetime
from typing import Optional


class Budget:
    """예산 모델"""

    def __init__(
        self,
        id: str,
        name: str,
        amount: float,
        category: str,
        user_id: str,
        spent: float = 0.0,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.name = name
        self.amount = amount
        self.category = category
        self.user_id = user_id
        self.spent = spent
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()

    def to_dict(self):
        """딕셔너리로 변환"""
        return {
            "id": self.id,
            "name": self.name,
            "amount": self.amount,
            "category": self.category,
            "user_id": self.user_id,
            "spent": self.spent,
            "remaining": self.amount - self.spent,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
