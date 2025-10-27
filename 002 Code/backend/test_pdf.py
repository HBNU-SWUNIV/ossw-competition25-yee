"""PDF 생성 테스트 스크립트"""
import asyncio
import sys
import os
from datetime import datetime

# 프로젝트 루트를 Python 경로에 추가
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.services.pdf_service import pdf_service


async def test_pdf_generation():
    """PDF 생성 테스트"""
    try:
        print("PDF 생성 테스트 시작...")
        
        # 테스트용 지출 데이터
        test_expense = {
            "id": "test_expense_123",
            "store_name": "스타벅스 강남점",
            "store_address": "서울특별시 강남구 테헤란로 152, 1층",
            "store_phone_number": "02-1234-5678",
            "amount": 15000,
            "date": datetime.now(),
            "category": "식비",
            "description": "팀 회의용 커피 구매"
        }
        
        # 테스트용 영수증 데이터 (이미지 없음)
        test_receipt = {
            "id": "test_receipt_123",
            "image_url": None  # 이미지 없이 테스트
        }
        
        print("PDF 생성 중...")
        pdf_bytes = await pdf_service.generate_expense_pdf(test_expense, test_receipt)
        
        # PDF 파일로 저장
        output_path = "test_expense.pdf"
        with open(output_path, "wb") as f:
            f.write(pdf_bytes)
        
        print(f"✅ PDF 생성 성공!")
        print(f"파일 크기: {len(pdf_bytes)} bytes")
        print(f"저장 위치: {os.path.abspath(output_path)}")
        
        return True
        
    except Exception as e:
        print(f"❌ PDF 생성 실패: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = asyncio.run(test_pdf_generation())
    if success:
        print("\n🎉 PDF 기능이 정상적으로 작동합니다!")
    else:
        print("\n💥 PDF 기능에 문제가 있습니다. 오류를 확인하세요.")