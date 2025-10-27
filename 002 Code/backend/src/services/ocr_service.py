import io
import os
import re
import cv2
from datetime import datetime
from typing import Dict, Any, Optional
from PIL import Image
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeResult
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()


class OCRService:
    """Azure Document Intelligence 기반 영수증 OCR 서비스"""

    def __init__(self):
        """Azure Document Intelligence 클라이언트 초기화"""
        print("[OCR] Initializing Azure Document Intelligence...")

        # 환경 변수에서 Azure 자격증명 가져오기
        self.endpoint = os.getenv("AZURE_OCR_ENDPOINT")
        self.key = os.getenv("AZURE_OCR_KEY")

        if not self.endpoint or not self.key:
            raise ValueError(
                "Azure OCR 자격증명이 설정되지 않았습니다.\n"
                ".env 파일에 다음을 추가하세요:\n"
                "AZURE_OCR_ENDPOINT=your-endpoint-url\n"
                "AZURE_OCR_KEY=your-api-key"
            )

        self.client = DocumentIntelligenceClient(
            endpoint=self.endpoint,
            credential=AzureKeyCredential(self.key)
        )
        self.file_limit_mb = 4
        print("[OCR] Azure Document Intelligence initialized successfully")

    async def process_receipt(self, image_data: bytes = None, image_path: str = None) -> Dict[str, Any]:
        """
        영수증 이미지를 Azure OCR 처리하여 구조화된 데이터 추출

        Args:
            image_data: 이미지 바이트 데이터
            image_path: 이미지 파일 경로 (선택)

        Returns:
            OCR 결과 딕셔너리
        """
        try:
            # 이미지 데이터 준비
            if image_data:
                image_bytes = image_data
            elif image_path:
                with open(image_path, "rb") as f:
                    image_bytes = f.read()
            else:
                raise ValueError("image_data 또는 image_path가 필요합니다")

            # 파일 크기 확인 및 압축
            file_size_mb = len(image_bytes) / (1024 * 1024)
            content_type = "application/octet-stream"

            if file_size_mb > self.file_limit_mb:
                print(f"[OCR] 파일 크기({file_size_mb:.2f} MB)가 {self.file_limit_mb}MB를 초과합니다. 압축을 시도합니다.")
                image_bytes = self._compress_image(image_bytes)
                file_size_mb = len(image_bytes) / (1024 * 1024)
                print(f"[OCR] 압축 완료. (새 용량: {file_size_mb:.2f} MB)")
                content_type = "image/jpeg"

            # Azure Document Intelligence API 호출
            print("[OCR] Azure Document Intelligence로 영수증 분석 중...")
            poller = self.client.begin_analyze_document(
                "prebuilt-receipt",
                body=image_bytes,
                content_type=content_type
            )

            result: AnalyzeResult = poller.result()

            # Azure OCR 결과 파싱
            parsed_data = self._parse_azure_receipt(result)

            return {
                "status": "success",
                "data": parsed_data,
                "raw_ocr_response": {
                    "engine": "Azure Document Intelligence",
                    "confidence": result.documents[0].confidence if result.documents else 0
                }
            }

        except Exception as e:
            print(f"[OCR ERROR] {str(e)}")
            return {
                "status": "error",
                "message": str(e),
                "data": None
            }

    def _compress_image(self, image_bytes: bytes) -> bytes:
        """
        이미지 압축 (4MB 초과 시)

        Args:
            image_bytes: 원본 이미지 바이트

        Returns:
            압축된 이미지 바이트
        """
        try:
            image = cv2.imdecode(
                __import__('numpy').frombuffer(image_bytes, __import__('numpy').uint8),
                cv2.IMREAD_COLOR
            )
            if image is None:
                return image_bytes

            encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 85]
            result, encoded_image = cv2.imencode('.jpg', image, encode_param)

            if result:
                return encoded_image.tobytes()
            return image_bytes
        except Exception as e:
            print(f"[OCR] 이미지 압축 실패: {str(e)}")
            return image_bytes

    def _parse_azure_receipt(self, result: AnalyzeResult) -> Dict[str, Any]:
        """
        Azure Document Intelligence 결과에서 영수증 정보 추출

        Args:
            result: Azure AnalyzeResult 객체

        Returns:
            파싱된 영수증 데이터
        """
        if not result.documents or len(result.documents) == 0:
            raise ValueError("영수증 정보를 추출할 수 없습니다")

        receipt = result.documents[0]
        fields = receipt.fields

        # 1. 상호명 추출 (여러 필드 시도 + 원본 텍스트에서 추출)
        store_name = (
            self._get_field_value(fields.get("MerchantName")) or
            self._get_field_value(fields.get("Merchant")) or
            self._extract_merchant_from_lines(result)
        )

        # 2. 주소 추출
        store_address = self._get_field_value(fields.get("MerchantAddress"))

        # 3. 전화번호 추출
        store_phone_number = self._get_field_value(fields.get("MerchantPhoneNumber"))

        # 4. 날짜 추출
        date = self._extract_azure_date(
            fields.get("TransactionDate"),
            fields.get("TransactionTime")
        )

        # 5. 총액 추출
        total_amount = self._extract_azure_total(fields.get("Total"))

        print(f"[OCR] 추출 결과 - 상호명: {store_name}, 주소: {store_address}, 전화: {store_phone_number}, 총액: {total_amount}")

        return {
            "store_name": store_name or "미지정",
            "store_address": store_address or "",
            "store_phone_number": store_phone_number or "",
            "date": date,
            "total_amount": total_amount
        }

    def _get_field_value(self, field) -> Optional[str]:
        """Azure 필드에서 값 추출"""
        if field is None:
            return None
        if hasattr(field, 'content'):
            return field.content
        if hasattr(field, 'value'):
            return str(field.value)
        return None

    def _extract_azure_date(self, date_field, time_field) -> datetime:
        """Azure에서 추출한 날짜-시간 필드 파싱"""
        try:
            date_str = self._get_field_value(date_field) or ""
            time_str = self._get_field_value(time_field) or ""

            # 날짜 형식: YYYY-MM-DD
            if date_str:
                date_obj = datetime.strptime(date_str, "%Y-%m-%d")

                # 시간 형식: HH:MM 또는 HH:MM:SS
                if time_str:
                    try:
                        time_obj = datetime.strptime(time_str, "%H:%M:%S")
                    except:
                        try:
                            time_obj = datetime.strptime(time_str, "%H:%M")
                        except:
                            time_obj = datetime.strptime("00:00:00", "%H:%M:%S")

                    date_obj = date_obj.replace(
                        hour=time_obj.hour,
                        minute=time_obj.minute,
                        second=time_obj.second
                    )

                return date_obj
        except Exception as e:
            print(f"[OCR] 날짜 파싱 오류: {str(e)}")

        return datetime.utcnow()

    def _extract_azure_total(self, total_field) -> float:
        """Azure에서 추출한 총액 필드 파싱"""
        try:
            if total_field is None:
                return 0.0

            # Amount 객체인 경우
            if hasattr(total_field, 'value') and hasattr(total_field.value, 'amount'):
                return float(total_field.value.amount)

            # 문자열인 경우
            if hasattr(total_field, 'content'):
                content = total_field.content
                # 숫자만 추출
                numbers = re.findall(r'\d+(?:,\d+)*(?:\.\d+)?', content.replace(',', ''))
                if numbers:
                    return float(numbers[-1])

            return 0.0
        except Exception as e:
            print(f"[OCR] 총액 파싱 오류: {str(e)}")
            return 0.0

    def _extract_merchant_from_lines(self, result: AnalyzeResult) -> Optional[str]:
        """
        OCR 원본 텍스트에서 상호명 추출 (fallback)
        영수증 상단의 첫 번째 텍스트 라인을 상호명으로 추정
        """
        try:
            if not result.pages or len(result.pages) == 0:
                return None

            page = result.pages[0]
            if not page.lines or len(page.lines) == 0:
                return None

            # 제외할 패턴 목록
            exclude_patterns = [
                r'^\[.*\]$',  # [영수증], [Receipt] 등 대괄호로 감싸진 텍스트
                r'^영수증$',  # "영수증" 단독
                r'^receipt$',  # "receipt" 단독 (대소문자 무시)
                r'^\d{4}[-/]\d{2}[-/]\d{2}',  # 날짜 패턴
                r'^[\d,]+원?$',  # 금액 패턴
                r'^[\d\s\-\(\)]+$',  # 숫자와 특수문자만
            ]

            # 상위 5개 라인 확인 (영수증은 보통 상단에 상호명이 있음)
            for line in page.lines[:5]:
                content = line.content.strip()

                # 빈 문자열이나 너무 짧은 경우 제외
                if not content or len(content) < 2:
                    continue

                # 제외 패턴 확인
                should_exclude = False
                for pattern in exclude_patterns:
                    if re.match(pattern, content, re.IGNORECASE):
                        should_exclude = True
                        break

                if not should_exclude:
                    print(f"[OCR] 원본 텍스트에서 상호명 추출: {content}")
                    return content

            return None
        except Exception as e:
            print(f"[OCR] 원본 텍스트 파싱 오류: {str(e)}")
            return None

ocr_service = OCRService()
