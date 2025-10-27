"""기존 지출 데이터 확인 스크립트"""
import asyncio
import sys
import os

# 프로젝트 루트를 Python 경로에 추가
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.services.expense_service import expense_service
from src.core.firebase import firebase_client

async def check_expenses():
    """기존 지출 데이터 확인"""
    try:
        print("기존 지출 데이터 확인 중...")
        
        # 모든 사용자의 지출 조회 (테스트용)
        db = firebase_client.db
        expenses_collection = db.collection("expenses")
        docs = expenses_collection.limit(10).stream()
        
        expenses = []
        for doc in docs:
            expense_data = doc.to_dict()
            expense_data["id"] = doc.id
            expenses.append(expense_data)
        
        if not expenses:
            print("❌ 지출 데이터가 없습니다.")
            return
            
        print(f"✅ 총 {len(expenses)}개의 지출 데이터 발견")
        print("\n📋 지출 목록:")
        
        for expense in expenses:
            print(f"\n- ID: {expense['id']}")
            print(f"  상호명: {expense.get('store_name', '정보 없음')}")
            print(f"  주소: {expense.get('store_address', '정보 없음')}")
            print(f"  연락처: {expense.get('store_phone_number', '정보 없음')}")
            print(f"  금액: ₩{expense.get('amount', 0):,}")
            print(f"  카테고리: {expense.get('category', '정보 없음')}")
            
    except Exception as e:
        print(f"❌ 오류 발생: {str(e)}")

if __name__ == "__main__":
    asyncio.run(check_expenses())