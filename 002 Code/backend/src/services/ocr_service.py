import requests
from typing import Dict, Any
from src.core.config import settings


class OCRService:
    """NAVER Clover OCR 서비스"""

    def __init__(self):
        self.api_url = settings.NAVER_OCR_API_URL
        self.secret_key = settings.NAVER_OCR_SECRET_KEY

    async def process_receipt(self, image_data: bytes) -> Dict[str, Any]:
        """
        영수증 이미지를 OCR 처리

        Args:
            image_data: 이미지 바이트 데이터

        Returns:
            OCR 결과 딕셔너리
        """
        try:
            # TODO: NAVER Clover OCR API 호출 구현
            # headers = {
            #     "X-OCR-SECRET": self.secret_key,
            #     "Content-Type": "application/json"
            # }
            # response = requests.post(self.api_url, headers=headers, data=image_data)

            # 임시 반환값
            return {
                "status": "success",
                "data": {
                    "date": "2024-01-01",
                    "total_amount": 50000,
                    "items": [
                        {"name": "상품1", "price": 20000},
                        {"name": "상품2", "price": 30000}
                    ],
                    "store_name": "테스트 상점"
                }
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }


ocr_service = OCRService()
