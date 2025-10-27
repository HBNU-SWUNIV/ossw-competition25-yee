"""주소와 연락처가 포함된 샘플 지출 추가"""
import asyncio
import sys
import os
from datetime import datetime

# 프로젝트 루트를 Python 경로에 추가
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.services.expense_service import expense_service
from src.core.firebase import firebase_client

async def add_sample_expense():
    """샘플 지출 데이터 추가"""
    try:
        print("샘플 지출 데이터 추가 중...")
        
        # 테스트 사용자 ID 찾기
        db = firebase_client.db
        users = db.collection("users").where("email", "==", "test@example.com").limit(1).stream()
        
        test_user_id = None
        for doc in users:
            test_user_id = doc.id
            break
            
        if not test_user_id:
            print("❌ 테스트 사용자를 찾을 수 없습니다.")
            print("다음 명령어로 테스트 사용자를 먼저 생성하세요:")
            print("python create_test_user.py")
            return
            
        print(f"✅ 테스트 사용자 ID: {test_user_id}")
        
        # 샘플 지출 데이터
        sample_expense = {
            "user_id": test_user_id,
            "receipt_id": f"sample_{int(datetime.now().timestamp())}",
            "store_name": "스타벅스 강남점",
            "store_address": "서울특별시 강남구 테헤란로 152, 1층",
            "store_phone_number": "02-1234-5678",
            "amount": 15000.0,
            "date": datetime.now(),
            "category": "식비",
            "description": "팀 회의용 커피 구매",
            "item_name": "아메리카노 3잔"
        }
        
        # 지출 생성
        expense = await expense_service.create_expense(**sample_expense)
        
        print("✅ 샘플 지출 데이터가 성공적으로 추가되었습니다!")
        print(f"- 상호명: {expense['store_name']}")
        print(f"- 주소: {expense['store_address']}")
        print(f"- 연락처: {expense['store_phone_number']}")
        print(f"- 금액: ₩{expense['amount']:,}")
        
        print("\n🎉 이제 프론트엔드에서 주소와 연락처가 표시됩니다!")
        
    except Exception as e:
        print(f"❌ 오류 발생: {str(e)}")

if __name__ == "__main__":
    asyncio.run(add_sample_expense())