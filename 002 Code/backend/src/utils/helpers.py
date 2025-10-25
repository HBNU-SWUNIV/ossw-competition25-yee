from datetime import datetime
from typing import Any, Dict


def get_current_timestamp() -> str:
    """현재 타임스탬프 반환"""
    return datetime.utcnow().isoformat()


def format_currency(amount: float) -> str:
    """금액을 한국 원화 형식으로 포맷"""
    return f"₩{amount:,.0f}"


def validate_budget_data(data: Dict[str, Any]) -> bool:
    """예산 데이터 유효성 검증"""
    required_fields = ["name", "amount", "category"]
    return all(field in data for field in required_fields)


def validate_receipt_data(data: Dict[str, Any]) -> bool:
    """영수증 데이터 유효성 검증"""
    required_fields = ["date", "total_amount", "items"]
    return all(field in data for field in required_fields)
