from datetime import datetime
from typing import Optional, List, Dict


class Receipt:
    """영수증 모델"""

    def __init__(
        self,
        id: str,
        user_id: str,
        budget_id: str,
        store_name: str,
        total_amount: float,
        purchase_date: datetime,
        items: List[Dict[str, any]],
        image_url: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.user_id = user_id
        self.budget_id = budget_id
        self.store_name = store_name
        self.total_amount = total_amount
        self.purchase_date = purchase_date
        self.items = items
        self.image_url = image_url
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()

    def to_dict(self):
        """딕셔너리로 변환"""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "budget_id": self.budget_id,
            "store_name": self.store_name,
            "total_amount": self.total_amount,
            "purchase_date": self.purchase_date.isoformat(),
            "items": self.items,
            "image_url": self.image_url,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
