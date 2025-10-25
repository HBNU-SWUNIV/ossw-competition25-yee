from datetime import datetime
from typing import Optional


class User:
    """사용자 모델"""

    def __init__(
        self,
        id: str,
        email: str,
        name: str,
        hashed_password: str,
        role: str = "user",  # user, admin
        is_active: bool = True,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.email = email
        self.name = name
        self.hashed_password = hashed_password
        self.role = role
        self.is_active = is_active
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()

    def to_dict(self, include_password: bool = False):
        """딕셔너리로 변환"""
        data = {
            "id": self.id,
            "email": self.email,
            "name": self.name,
            "role": self.role,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
        if include_password:
            data["hashed_password"] = self.hashed_password
        return data
