"""테스트용 지출 데이터 생성 스크립트"""
import asyncio
import sys
import os
from datetime import datetime, timedelta
import random

# 프로젝트 루트를 Python 경로에 추가
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.services.expense_service import expense_service
from src.core.firebase import firebase_client

# 테스트 데이터
test_expenses = [
    {
        "store_name": "스타벅스 강남점",
        "store_address": "서울특별시 강남구 테헤란로 152",
        "store_phone_number": "02-1234-5678",
        "amount": 15000,
        "category": "식비",
        "description": "팀 회의용 커피"
    },
    {
        "store_name": "교보문고 광화문점",
        "store_address": "서울특별시 종로구 종로 1",
        "store_phone_number": "02-2222-3333",
        "amount": 25000,
        "category": "사무용품",
        "description": "업무용 도서 구매"
    },
    {
        "store_name": "맥도날드 홍대점",
        "store_address": "서울특별시 마포구 홍익로 3길 20",
        "store_phone_number": "02-3333-4444",
        "amount": 8500,
        "category": "식비",
        "description": "점심 식사"
    },
    {
        "store_name": "GS25 편의점",
        "store_address": "서울특별시 서초구 서초대로 77길 3",
        "store_phone_number": "02-4444-5555",
        "amount": 3200,
        "category": "기타",
        "description": "사무용품 구매"
    },
    {
        "store_name": "올리브영 강남역점",
        "store_address": "서울특별시 강남구 강남대로 390",
        "store_phone_number": "02-5555-6666",
        "amount": 12000,
        "category": "기타",
        "description": "개인용품 구매"
    }
]

async def create_test_expenses():
    """테스트 지출 데이터 생성"""
    try:
        print("테스트 지출 데이터 생성 시작...")
        
        # 테스트 사용자 ID 찾기
        db = firebase_client.db
        users = db.collection("users").where("email", "==", "test@example.com").limit(1).stream()
        
        test_user_id = None
        for doc in users:
            test_user_id = doc.id
            break
            
        if not test_user_id:
            print("❌ 테스트 사용자를 찾을 수 없습니다. 먼저 create_test_user.py를 실행하세요.")
            return
            
        print(f"✅ 테스트 사용자 ID: {test_user_id}")
        
        for i, expense_data in enumerate(test_expenses):
            # 최근 30일 내의 랜덤 날짜 생성
            days_ago = random.randint(1, 30)
            expense_date = datetime.now() - timedelta(days=days_ago)
            
            # 지출 생성
            expense = await expense_service.create_expense(
                user_id=test_user_id,
                receipt_id=f"test_receipt_{i+1}_{int(datetime.now().timestamp())}",
                store_name=expense_data["store_name"],
                store_address=expense_data["store_address"],
                store_phone_number=expense_data["store_phone_number"],
                amount=expense_data["amount"],
                date=expense_date,
                category=expense_data["category"],
                description=expense_data["description"]
            )
            
            print(f"✅ 지출 생성 완료: {expense_data['store_name']} - ₩{expense_data['amount']:,}")
        
        print(f"\n🎉 총 {len(test_expenses)}개의 테스트 지출 데이터가 생성되었습니다!")
        
        # 생성된 지출 목록 확인
        print("\n📋 생성된 지출 목록:")
        expenses = await expense_service.get_expenses(user_id=test_user_id, limit=10)
        
        for expense in expenses:
            print(f"- {expense['store_name']}: ₩{expense['amount']:,}")
            print(f"  주소: {expense.get('store_address', '정보 없음')}")
            print(f"  연락처: {expense.get('store_phone_number', '정보 없음')}")
            print()
            
    except Exception as e:
        print(f"❌ 오류 발생: {str(e)}")

if __name__ == "__main__":
    asyncio.run(create_test_expenses())