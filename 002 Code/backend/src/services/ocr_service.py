import io
import re
from datetime import datetime
from typing import Dict, Any, List
from paddleocr import PaddleOCR
from PIL import Image


class OCRService:
    """PaddleOCR 기반 영수증 OCR 서비스 (오픈소스)"""

    def __init__(self):
        # PaddleOCR 초기화 (한글 + 영어)
        # use_angle_cls=True: 이미지 회전 감지 및 보정
        # lang='korean': 한글 모델 사용
        print("[OCR] Initializing PaddleOCR...")
        self.ocr = PaddleOCR(
            use_angle_cls=True,
            lang='korean',
            show_log=False,
            use_gpu=False  # CPU 사용 (GPU가 있으면 True로 변경)
        )
        print("[OCR] PaddleOCR initialized successfully")

    async def process_receipt(self, image_data: bytes = None, image_path: str = None) -> Dict[str, Any]:
        """
        영수증 이미지를 OCR 처리하여 구조화된 데이터 추출

        Args:
            image_data: 이미지 바이트 데이터
            image_path: 이미지 파일 경로 (선택)

        Returns:
            OCR 결과 딕셔너리
        """
        try:
            # 이미지 로드
            if image_data:
                image = Image.open(io.BytesIO(image_data))
            elif image_path:
                image = Image.open(image_path)
            else:
                raise ValueError("image_data 또는 image_path가 필요합니다")

            # 이미지를 numpy array로 변환
            import numpy as np
            image_np = np.array(image)

            # PaddleOCR 실행
            print("[OCR] Running PaddleOCR on image...")
            result = self.ocr.ocr(image_np, cls=True)

            # OCR 결과에서 텍스트 추출
            if not result or not result[0]:
                return {
                    "status": "error",
                    "message": "텍스트를 찾을 수 없습니다",
                    "data": None
                }

            # 모든 텍스트 라인 추출
            all_text_lines = []
            for line in result[0]:
                text = line[1][0]  # (bbox, (text, confidence))
                confidence = line[1][1]
                all_text_lines.append({
                    "text": text,
                    "confidence": confidence
                })

            print(f"[OCR] Extracted {len(all_text_lines)} text lines")

            # 영수증 정보 파싱
            parsed_data = self._parse_receipt(all_text_lines)

            return {
                "status": "success",
                "data": parsed_data,
                "raw_ocr_response": {
                    "engine": "PaddleOCR",
                    "version": "2.7.0",
                    "lines": all_text_lines
                }
            }

        except Exception as e:
            print(f"[OCR ERROR] {str(e)}")
            return {
                "status": "error",
                "message": str(e),
                "data": None
            }

    def _parse_receipt(self, text_lines: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        OCR 텍스트 라인에서 영수증 정보 추출

        Args:
            text_lines: OCR로 추출한 텍스트 라인 리스트

        Returns:
            파싱된 영수증 데이터
        """
        # 전체 텍스트 결합
        full_text = "\n".join([line["text"] for line in text_lines])

        # 1. 상호명 추출 (보통 첫 줄 또는 두 번째 줄)
        store_name = self._extract_store_name(text_lines)

        # 2. 날짜 추출
        date = self._extract_date(full_text)

        # 3. 금액 추출
        amounts = self._extract_amounts(text_lines)

        # 4. 총액 추출 (가장 큰 금액 또는 "합계", "총액" 근처의 금액)
        total_amount = self._extract_total_amount(text_lines, amounts)

        # 5. 품목 추출 (금액이 있는 라인들)
        items = self._extract_items(text_lines, amounts)

        return {
            "store_name": store_name,
            "date": date,
            "total_amount": total_amount,
            "items": items
        }

    def _extract_store_name(self, text_lines: List[Dict[str, Any]]) -> str:
        """상호명 추출 (상위 2-3줄에서 가장 신뢰도 높은 텍스트)"""
        if not text_lines:
            return "알 수 없음"

        # 상위 3줄 중 가장 긴 텍스트를 상호명으로 추정
        top_lines = text_lines[:3]
        store_candidates = [
            line["text"] for line in top_lines
            if len(line["text"]) > 2 and line["confidence"] > 0.8
        ]

        if store_candidates:
            return max(store_candidates, key=len)
        return text_lines[0]["text"] if text_lines else "알 수 없음"

    def _extract_date(self, text: str) -> str:
        """날짜 추출 (YYYY-MM-DD, YYYY.MM.DD, YYYY/MM/DD 등)"""
        # 날짜 패턴들
        date_patterns = [
            r'(\d{4})[-.년/\s](\d{1,2})[-.월/\s](\d{1,2})',  # 2024-01-15, 2024년 1월 15일
            r'(\d{2})[-.년/\s](\d{1,2})[-.월/\s](\d{1,2})',  # 24-01-15
        ]

        for pattern in date_patterns:
            match = re.search(pattern, text)
            if match:
                year, month, day = match.groups()
                # 2자리 연도를 4자리로 변환
                if len(year) == 2:
                    year = f"20{year}"
                try:
                    # 유효한 날짜인지 확인
                    date_obj = datetime(int(year), int(month), int(day))
                    return date_obj.strftime("%Y-%m-%d")
                except ValueError:
                    continue

        # 날짜를 찾지 못하면 오늘 날짜 반환
        return datetime.now().strftime("%Y-%m-%d")

    def _extract_amounts(self, text_lines: List[Dict[str, Any]]) -> List[int]:
        """모든 금액 추출"""
        amounts = []
        for line in text_lines:
            text = line["text"]
            # 금액 패턴: 숫자 + 원, 또는 ,로 구분된 숫자
            amount_matches = re.findall(r'([\d,]+)\s*원?', text)
            for match in amount_matches:
                try:
                    amount = int(match.replace(',', ''))
                    if 100 <= amount <= 10000000:  # 100원 ~ 1000만원 범위
                        amounts.append(amount)
                except ValueError:
                    continue
        return amounts

    def _extract_total_amount(self, text_lines: List[Dict[str, Any]], amounts: List[int]) -> int:
        """총액 추출 (합계, 총액, 받을금액 등의 키워드 근처)"""
        total_keywords = ['합계', '총액', '받을금액', '결제금액', 'total', 'Total']

        # 키워드가 있는 라인에서 금액 찾기
        for line in text_lines:
            text = line["text"]
            if any(keyword in text for keyword in total_keywords):
                # 해당 라인에서 금액 추출
                amount_matches = re.findall(r'([\d,]+)\s*원?', text)
                for match in amount_matches:
                    try:
                        amount = int(match.replace(',', ''))
                        if 100 <= amount <= 10000000:
                            return amount
                    except ValueError:
                        continue

        # 키워드를 못 찾으면 가장 큰 금액 반환
        if amounts:
            return max(amounts)
        return 0

    def _extract_items(self, text_lines: List[Dict[str, Any]], amounts: List[int]) -> List[Dict[str, Any]]:
        """품목 추출 (상품명 + 금액 조합)"""
        items = []
        skip_keywords = ['합계', '총액', '받을금액', '결제금액', '카드', '현금', '부가세', 'VAT']

        for i, line in enumerate(text_lines):
            text = line["text"]

            # 스킵할 라인
            if any(keyword in text for keyword in skip_keywords):
                continue

            # 금액이 포함된 라인
            amount_matches = re.findall(r'([\d,]+)\s*원?', text)
            for match in amount_matches:
                try:
                    amount = int(match.replace(',', ''))
                    if 100 <= amount <= 10000000 and amount in amounts:
                        # 상품명 추출 (금액 앞의 텍스트)
                        item_name = re.sub(r'[\d,]+\s*원?', '', text).strip()
                        if len(item_name) > 1:
                            items.append({
                                "name": item_name,
                                "price": amount
                            })
                            break
                except ValueError:
                    continue

        # 품목이 없으면 더미 데이터 생성
        if not items and amounts:
            items = [{
                "name": "상품",
                "price": amounts[0] if amounts else 0
            }]

        return items


ocr_service = OCRService()
