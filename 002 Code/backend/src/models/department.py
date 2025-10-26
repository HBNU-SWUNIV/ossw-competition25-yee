from datetime import datetime
from typing import Optional


class Department:
    """부서 모델"""

    def __init__(
        self,
        id: str,
        name: str,
        description: Optional[str] = None,
        budget_limit: float = 0.0,
        manager_id: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ):
        self.id = id
        self.name = name
        self.description = description
        self.budget_limit = budget_limit
        self.manager_id = manager_id
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()

    def to_dict(self) -> dict:
        """딕셔너리로 변환"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "budget_limit": self.budget_limit,
            "manager_id": self.manager_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    @staticmethod
    def from_dict(data: dict) -> "Department":
        """딕셔너리에서 객체 생성"""
        return Department(
            id=data.get("id", ""),
            name=data.get("name", ""),
            description=data.get("description"),
            budget_limit=data.get("budget_limit", 0.0),
            manager_id=data.get("manager_id"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
        )
