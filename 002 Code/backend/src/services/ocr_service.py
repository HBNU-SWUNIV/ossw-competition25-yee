import requests
import random
from datetime import datetime, timedelta
from typing import Dict, Any, List
from src.core.config import settings


class OCRService:
    """NAVER Clover OCR 서비스"""

    def __init__(self):
        self.api_url = settings.NAVER_OCR_API_URL
        self.secret_key = settings.NAVER_OCR_SECRET_KEY
        # API 키가 없거나 더미 값이면 Mock 사용
        self.use_mock = (
            not self.api_url or
            not self.secret_key or
            "your-ocr-api-url" in str(self.api_url) or
            "your-secret-key" in str(self.secret_key)
        )

    def _generate_mock_data(self) -> Dict[str, Any]:
        """
        테스트용 Mock OCR 데이터 생성
        실제 영수증과 유사한 더미 데이터를 반환
        """
        # 다양한 상점 샘플
        stores = [
            {"name": "스타벅스 강남점", "category": "식비"},
            {"name": "다이소 홍대점", "category": "사무용품"},
            {"name": "삼겹살 맛집", "category": "회식"},
            {"name": "GS25 편의점", "category": "식비"},
            {"name": "맥도날드 역삼점", "category": "식비"},
            {"name": "문구마트", "category": "사무용품"},
            {"name": "카카오택시", "category": "교통비"},
            {"name": "CU 편의점", "category": "식비"},
        ]

        store = random.choice(stores)

        # 상점에 맞는 품목 생성
        items_by_category = {
            "식비": [
                {"name": "아메리카노", "price": 4500},
                {"name": "카페라떼", "price": 5000},
                {"name": "샌드위치", "price": 6500},
                {"name": "도시락", "price": 5500},
                {"name": "김밥", "price": 3000},
            ],
            "사무용품": [
                {"name": "볼펜 세트", "price": 5000},
                {"name": "노트", "price": 3000},
                {"name": "파일", "price": 2500},
                {"name": "테이프", "price": 1500},
            ],
            "회식": [
                {"name": "삼겹살", "price": 35000},
                {"name": "소주", "price": 5000},
                {"name": "맥주", "price": 5000},
                {"name": "공기밥", "price": 2000},
            ],
            "교통비": [
                {"name": "택시 요금", "price": 15000},
            ]
        }

        # 카테고리에 맞는 품목 선택
        category = store["category"]
        available_items = items_by_category.get(category, items_by_category["식비"])

        # 1~3개의 품목 무작위 선택
        num_items = random.randint(1, min(3, len(available_items)))
        selected_items = random.sample(available_items, num_items)

        # 총액 계산
        total_amount = sum(item["price"] for item in selected_items)

        # 날짜 생성 (최근 30일 이내)
        days_ago = random.randint(0, 30)
        purchase_date = (datetime.now() - timedelta(days=days_ago)).strftime("%Y-%m-%d")

        return {
            "status": "success",
            "data": {
                "store_name": store["name"],
                "date": purchase_date,
                "total_amount": total_amount,
                "items": selected_items,
                "category_hint": category  # 분류 힌트 (실제 OCR에서는 없을 수 있음)
            },
            "raw_ocr_response": {
                # 실제 NAVER OCR API 응답 형식 시뮬레이션
                "version": "V2",
                "requestId": f"mock-{datetime.now().timestamp()}",
                "timestamp": int(datetime.now().timestamp() * 1000),
                "images": [{
                    "receipt": {
                        "meta": {
                            "estimatedLanguage": "ko"
                        },
                        "result": {
                            "storeInfo": {
                                "name": {"text": store["name"]}
                            },
                            "paymentInfo": {
                                "date": {"text": purchase_date},
                                "totalPrice": {"price": {"formatted": {"value": str(total_amount)}}}
                            },
                            "subResults": [{
                                "items": [{"name": {"text": item["name"]},
                                          "price": {"price": {"formatted": {"value": str(item["price"])}}}}
                                         for item in selected_items]
                            }]
                        }
                    }
                }]
            }
        }

    async def process_receipt(self, image_data: bytes = None, image_path: str = None) -> Dict[str, Any]:
        """
        영수증 이미지를 OCR 처리

        Args:
            image_data: 이미지 바이트 데이터
            image_path: 이미지 파일 경로 (선택)

        Returns:
            OCR 결과 딕셔너리
        """
        try:
            # Mock 데이터 사용 (API 키가 없는 경우)
            if self.use_mock:
                print("[WARN] OCR API key not configured, using Mock data")
                return self._generate_mock_data()

            # 실제 NAVER Clover OCR API 호출
            # TODO: API 키가 발급되면 아래 코드 활성화
            headers = {
                "X-OCR-SECRET": self.secret_key,
                "Content-Type": "application/json"
            }

            # 이미지 데이터 준비
            files = {"file": image_data} if image_data else None

            response = requests.post(self.api_url, headers=headers, files=files)
            response.raise_for_status()

            ocr_result = response.json()

            # NAVER OCR 응답을 표준 형식으로 변환
            return self._parse_naver_ocr_response(ocr_result)

        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
                "data": None
            }

    def _parse_naver_ocr_response(self, ocr_response: Dict[str, Any]) -> Dict[str, Any]:
        """
        NAVER Clover OCR API 응답을 표준 형식으로 파싱

        Args:
            ocr_response: NAVER OCR API 원본 응답

        Returns:
            표준 형식의 영수증 데이터
        """
        try:
            # NAVER OCR 응답 구조에 맞춰 파싱
            # 실제 API 응답 구조에 따라 수정 필요
            receipt_data = ocr_response["images"][0]["receipt"]["result"]

            store_name = receipt_data.get("storeInfo", {}).get("name", {}).get("text", "")
            date = receipt_data.get("paymentInfo", {}).get("date", {}).get("text", "")
            total_amount = float(receipt_data.get("paymentInfo", {}).get("totalPrice", {})
                                .get("price", {}).get("formatted", {}).get("value", "0"))

            items = []
            for item in receipt_data.get("subResults", [{}])[0].get("items", []):
                items.append({
                    "name": item.get("name", {}).get("text", ""),
                    "price": float(item.get("price", {}).get("price", {})
                                  .get("formatted", {}).get("value", "0"))
                })

            return {
                "status": "success",
                "data": {
                    "store_name": store_name,
                    "date": date,
                    "total_amount": total_amount,
                    "items": items
                },
                "raw_ocr_response": ocr_response
            }

        except Exception as e:
            return {
                "status": "error",
                "message": f"OCR 응답 파싱 실패: {str(e)}",
                "data": None,
                "raw_ocr_response": ocr_response
            }


ocr_service = OCRService()
