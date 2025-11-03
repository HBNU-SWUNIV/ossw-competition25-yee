import io
import os
import requests
from datetime import datetime
from typing import Dict, Any, Optional
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image as RLImage, KeepTogether, PageBreak
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from PIL import Image


class PDFService:
    """PDF 생성 서비스 (한글 지원)"""

    def __init__(self):
        """한글 폰트 등록"""
        try:
            # Windows 기본 한글 폰트 등록 시도
            font_paths = [
                "C:/Windows/Fonts/malgun.ttf",  # 맑은 고딕
                "C:/Windows/Fonts/gulim.ttc",    # 굴림
                "C:/Windows/Fonts/NanumGothic.ttf",  # 나눔고딕
                "/usr/share/fonts/truetype/nanum/NanumGothic.ttf",  # Ubuntu
                "/System/Library/Fonts/AppleSDGothicNeo.ttc",  # macOS
                "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"  # Linux fallback
            ]

            self.font_name = None
            for font_path in font_paths:
                if os.path.exists(font_path):
                    try:
                        pdfmetrics.registerFont(TTFont('KoreanFont', font_path))
                        self.font_name = 'KoreanFont'
                        print(f"[PDF] 한글 폰트 등록 성공: {font_path}")
                        break
                    except Exception as e:
                        print(f"[PDF] 폰트 등록 실패 ({font_path}): {str(e)}")
                        continue

            if not self.font_name:
                print("[PDF] 한글 폰트를 찾을 수 없습니다. 기본 폰트 사용")
                self.font_name = 'DejaVuSans'
                
        except Exception as e:
            print(f"[PDF] 폰트 초기화 오류: {str(e)}")
            self.font_name = 'DejaVuSans'

    async def generate_expense_pdf(
        self,
        expense: Dict[str, Any],
        receipt: Optional[Dict[str, Any]] = None
    ) -> bytes:
        """
        개별 지출 내역 PDF 생성

        Args:
            expense: 지출 내역 데이터
            receipt: 영수증 데이터 (이미지 포함)

        Returns:
            PDF 바이트 데이터
        """
        try:
            buffer = io.BytesIO()
            doc = SimpleDocTemplate(
                buffer,
                pagesize=A4,
                rightMargin=20*mm,
                leftMargin=20*mm,
                topMargin=20*mm,
                bottomMargin=20*mm
            )

            # 문서 요소 리스트
            elements = []

            # 스타일 설정
            styles = self._get_styles()

            # 제목
            title = Paragraph("지출 내역서", styles['CustomTitle'])
            elements.append(title)
            elements.append(Spacer(1, 10*mm))

            # 영수증 이미지 추가 (있는 경우)
            if receipt and receipt.get("image_url"):
                try:
                    receipt_image = self._add_receipt_image(receipt["image_url"])
                    if receipt_image:
                        elements.append(receipt_image)
                        elements.append(Spacer(1, 5*mm))
                except Exception as e:
                    print(f"[PDF] 영수증 이미지 추가 실패: {str(e)}")

            # 지출 정보 테이블
            expense_info = self._create_expense_table(expense, styles)
            elements.append(expense_info)
            elements.append(Spacer(1, 10*mm))

            # 재무 정보 (총액 등)
            financial_info = self._create_financial_table(expense, styles)
            elements.append(financial_info)
            elements.append(Spacer(1, 10*mm))

            # 발행 정보
            footer_text = f"발행일: {datetime.now().strftime('%Y년 %m월 %d일')}"
            footer = Paragraph(footer_text, styles['Footer'])
            elements.append(footer)

            # PDF 생성
            doc.build(elements)
            pdf_bytes = buffer.getvalue()
            buffer.close()

            return pdf_bytes

        except Exception as e:
            raise Exception(f"PDF 생성 실패: {str(e)}")

    def _get_styles(self):
        """PDF 스타일 정의"""
        styles = getSampleStyleSheet()

        # 제목 스타일 - 이미 존재하면 덮어쓰기
        if 'CustomTitle' not in styles:
            styles.add(ParagraphStyle(
                name='CustomTitle',
                parent=styles['Heading1'],
                fontName=self.font_name,
                fontSize=24,
                alignment=TA_CENTER,
                spaceAfter=12,
                textColor=colors.HexColor('#1e3a8a')
            ))

        # 본문 스타일
        if 'Korean' not in styles:
            styles.add(ParagraphStyle(
                name='Korean',
                parent=styles['Normal'],
                fontName=self.font_name,
                fontSize=11,
                leading=14
            ))

        # 테이블 헤더 스타일
        if 'TableHeader' not in styles:
            styles.add(ParagraphStyle(
                name='TableHeader',
                parent=styles['Normal'],
                fontName=self.font_name,
                fontSize=11,
                textColor=colors.white,
                alignment=TA_CENTER
            ))

        # 테이블 셀 스타일
        if 'TableCell' not in styles:
            styles.add(ParagraphStyle(
                name='TableCell',
                parent=styles['Normal'],
                fontName=self.font_name,
                fontSize=10
            ))

        # 푸터 스타일
        if 'Footer' not in styles:
            styles.add(ParagraphStyle(
                name='Footer',
                parent=styles['Normal'],
                fontName=self.font_name,
                fontSize=9,
                alignment=TA_RIGHT,
                textColor=colors.grey
            ))

        return styles

    def _add_receipt_image(self, image_url: str) -> Optional[RLImage]:
        """영수증 이미지 다운로드 및 추가"""
        try:
            print(f"[PDF] 이미지 다운로드 시도: {image_url}")

            # 이미지 다운로드
            response = requests.get(image_url, timeout=15, verify=False)
            response.raise_for_status()

            # PIL로 이미지 처리
            img = Image.open(io.BytesIO(response.content))

            # EXIF 방향 정보 확인 및 자동 회전
            try:
                from PIL import ImageOps
                img = ImageOps.exif_transpose(img)
                print(f"[PDF] EXIF 방향 정보 기반 자동 회전 완료")
            except Exception as e:
                print(f"[PDF] EXIF 처리 건너뜀: {str(e)}")

            # RGB 모드로 변환 (RGBA나 다른 모드일 경우)
            if img.mode != 'RGB':
                img = img.convert('RGB')

            # 이미지 리사이즈 (같은 페이지에 들어갈 수 있도록 더 작게)
            # A4 페이지 너비에서 좌우 여백(40mm)을 빼면 약 170mm
            # 지출 내역과 같은 페이지에 들어가도록 작게 조정
            max_width_mm = 70  # mm (더 작게 조정)
            max_height_mm = 90  # mm (더 작게 조정)

            # mm를 픽셀로 변환 (150 DPI 기준으로 높여서 화질 개선)
            max_width_px = int(max_width_mm * 150 / 25.4)
            max_height_px = int(max_height_mm * 150 / 25.4)

            # 비율 유지하면서 리사이즈
            img.thumbnail((max_width_px, max_height_px), Image.Resampling.LANCZOS)

            # BytesIO로 변환 (quality를 95로 높여서 화질 개선)
            img_buffer = io.BytesIO()
            img.save(img_buffer, format='JPEG', quality=95)
            img_buffer.seek(0)

            # ReportLab Image 객체 생성 (thumbnail 후의 실제 크기 사용)
            actual_width = img.width
            actual_height = img.height

            # 픽셀을 mm로 변환
            width_mm = actual_width * 25.4 / 72
            height_mm = actual_height * 25.4 / 72

            rl_img = RLImage(img_buffer, width=width_mm*mm, height=height_mm*mm)

            print(f"[PDF] 이미지 추가 성공: {actual_width}x{actual_height} (원본에서 리사이즈됨)")
            return rl_img

        except Exception as e:
            print(f"[PDF] 이미지 로드 실패: {str(e)}")
            return None

    def _create_expense_table(self, expense: Dict[str, Any], styles) -> Table:
        """지출 정보 테이블 생성"""
        # 날짜 포맷팅
        expense_date = expense.get('date')
        if isinstance(expense_date, datetime):
            date_str = expense_date.strftime('%Y년 %m월 %d일')
        else:
            try:
                date_obj = datetime.fromisoformat(str(expense_date).replace('Z', '+00:00'))
                date_str = date_obj.strftime('%Y년 %m월 %d일')
            except:
                date_str = str(expense_date)

        data = [
            [Paragraph("항목", styles['TableHeader']), Paragraph("내용", styles['TableHeader'])],
            [Paragraph("상호명", styles['TableCell']), Paragraph(expense.get('store_name', '-'), styles['TableCell'])],
            [Paragraph("주소", styles['TableCell']), Paragraph(expense.get('store_address', '-'), styles['TableCell'])],
            [Paragraph("전화번호", styles['TableCell']), Paragraph(expense.get('store_phone_number', '-'), styles['TableCell'])],
            [Paragraph("날짜", styles['TableCell']), Paragraph(date_str, styles['TableCell'])],
            [Paragraph("카테고리", styles['TableCell']), Paragraph(expense.get('category', '-'), styles['TableCell'])],
            [Paragraph("설명", styles['TableCell']), Paragraph(expense.get('description', '-'), styles['TableCell'])],
        ]

        table = Table(data, colWidths=[50*mm, 120*mm])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3b82f6')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), self.font_name),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('TOPPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f3f4f6')])
        ]))

        return table

    def _create_financial_table(self, expense: Dict[str, Any], styles) -> Table:
        """재무 정보 테이블 생성"""
        amount = expense.get('amount', 0)
        amount_str = f"₩ {amount:,.0f}"

        data = [
            [Paragraph("총 금액", styles['TableHeader']), Paragraph(amount_str, styles['TableCell'])]
        ]

        table = Table(data, colWidths=[50*mm, 120*mm])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, 0), colors.HexColor('#10b981')),
            ('TEXTCOLOR', (0, 0), (0, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), self.font_name),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('FONTSIZE', (1, 0), (1, 0), 16),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('TOPPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1.5, colors.HexColor('#10b981')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))

        return table

    async def generate_report_pdf(self, expenses: list) -> bytes:
        """
        여러 지출 내역의 리포트 PDF 생성
        
        Args:
            expenses: 지출 내역 리스트
            
        Returns:
            PDF 바이트 데이터
        """
        try:
            buffer = io.BytesIO()
            doc = SimpleDocTemplate(
                buffer,
                pagesize=A4,
                rightMargin=20*mm,
                leftMargin=20*mm,
                topMargin=20*mm,
                bottomMargin=20*mm
            )

            elements = []
            styles = self._get_styles()

            # 제목
            title = Paragraph("지출 내역 리포트", styles['CustomTitle'])
            elements.append(title)
            elements.append(Spacer(1, 10*mm))

            # 요약 정보
            total_amount = sum(exp.get('amount', 0) for exp in expenses)
            avg_amount = total_amount / len(expenses) if len(expenses) > 0 else 0
            summary_data = [
                [Paragraph("항목", styles['TableHeader']), Paragraph("내용", styles['TableHeader'])],
                [Paragraph("총 지출 건수", styles['TableCell']), Paragraph(f"{len(expenses)}건", styles['TableCell'])],
                [Paragraph("총 지출 금액", styles['TableCell']), Paragraph(f"₩ {total_amount:,.0f}", styles['TableCell'])],
                [Paragraph("평균 지출", styles['TableCell']), Paragraph(f"₩ {avg_amount:,.0f}", styles['TableCell'])],
                [Paragraph("생성일", styles['TableCell']), Paragraph(datetime.now().strftime('%Y년 %m월 %d일'), styles['TableCell'])]
            ]

            summary_table = Table(summary_data, colWidths=[50*mm, 120*mm])
            summary_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3b82f6')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, -1), self.font_name),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('TOPPADDING', (0, 0), (-1, 0), 12),
                ('GRID', (0, 0), (-1, -1), 1, colors.grey),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f3f4f6')])
            ]))

            elements.append(summary_table)

            # 페이지 나누기 - 지출 내역을 다음 페이지부터 표시
            elements.append(PageBreak())

            # 각 지출 내역마다 정보와 영수증을 위아래로 표시
            for idx, expense in enumerate(expenses, 1):
                # 각 지출 내역을 함께 묶을 요소들
                expense_elements = []

                # 지출 내역 번호
                expense_date = expense.get('date')
                if isinstance(expense_date, datetime):
                    date_str = expense_date.strftime('%Y-%m-%d')
                else:
                    try:
                        date_obj = datetime.fromisoformat(str(expense_date).replace('Z', '+00:00'))
                        date_str = date_obj.strftime('%Y-%m-%d')
                    except:
                        date_str = str(expense_date)

                # 지출 내역 헤더
                header_text = f"{idx}. {date_str} | {expense.get('store_name', '-')} | ₩{expense.get('amount', 0):,}"
                header_para = Paragraph(header_text, styles['Korean'])
                expense_elements.append(header_para)
                expense_elements.append(Spacer(1, 2*mm))

                # 영수증 이미지 가져오기
                receipt_url = expense.get('receipt_url')
                receipt_img = None
                if receipt_url:
                    receipt_img = self._add_receipt_image(receipt_url)

                # 단일 큰 테이블로 정보와 영수증을 함께 배치
                # 왼쪽: 정보, 오른쪽: 영수증 이미지

                # 정보 셀 데이터 구성
                info_rows = [
                    [Paragraph("카테고리", styles['TableHeader']), Paragraph(expense.get('category', '-'), styles['TableCell'])],
                    [Paragraph("설명", styles['TableHeader']), Paragraph(expense.get('description', '-'), styles['TableCell'])]
                ]

                if expense.get('store_address'):
                    info_rows.append([Paragraph("주소", styles['TableHeader']), Paragraph(expense.get('store_address'), styles['TableCell'])])

                if expense.get('store_phone_number'):
                    info_rows.append([Paragraph("전화번호", styles['TableHeader']), Paragraph(expense.get('store_phone_number'), styles['TableCell'])])

                # 위아래 배치: 정보 테이블 위, 영수증 이미지 아래
                info_table = Table(info_rows, colWidths=[30*mm, 140*mm])
                info_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#3b82f6')),
                    ('TEXTCOLOR', (0, 0), (0, -1), colors.white),
                    ('BACKGROUND', (1, 0), (1, -1), colors.white),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (-1, -1), self.font_name),
                    ('FONTSIZE', (0, 0), (-1, -1), 9),
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ('TOPPADDING', (0, 0), (-1, -1), 6),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 6)
                ]))
                expense_elements.append(info_table)

                # 영수증 이미지 (정보 테이블 아래)
                if receipt_img:
                    expense_elements.append(Spacer(1, 3*mm))
                    # 영수증 이미지 레이블
                    img_label = Paragraph("영수증 이미지:", styles['Korean'])
                    expense_elements.append(img_label)
                    expense_elements.append(Spacer(1, 2*mm))
                    expense_elements.append(receipt_img)
                else:
                    expense_elements.append(Spacer(1, 2*mm))
                    no_receipt_text = Paragraph("(영수증 이미지 없음)", styles['TableCell'])
                    expense_elements.append(no_receipt_text)

                # 이 지출 내역의 모든 요소를 KeepTogether로 묶기
                elements.append(KeepTogether(expense_elements))

                # 항목 간 간격 (구분선 제거, 여백만)
                if idx < len(expenses):
                    elements.append(Spacer(1, 8*mm))

            # 발행 정보
            footer_text = f"발행일: {datetime.now().strftime('%Y년 %m월 %d일')}"
            footer = Paragraph(footer_text, styles['Footer'])
            elements.append(footer)

            # PDF 생성
            doc.build(elements)
            pdf_bytes = buffer.getvalue()
            buffer.close()

            return pdf_bytes

        except Exception as e:
            raise Exception(f"리포트 PDF 생성 실패: {str(e)}")


pdf_service = PDFService()
