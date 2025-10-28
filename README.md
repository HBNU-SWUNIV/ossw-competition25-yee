# Budgetly - 조직 예산 관리 시스템
소중한 오픈 소스 활용SW 경진대회
# 국립한밭대학교 YEE팀

## 주제
OCR을 활용한 조직예산 관리 PWA (경진대회 참여 주제)

## 팀 구성
- 20211893 임동건 컴퓨터공학과
- 20211929 정택준 컴퓨터공학과
- 20222562 사민경 컴퓨터공학과
- 20237142 전준 컴퓨터공학과

## Project Background
  - ### 개요
  Azure Document Intelligence OCR을 활용해 영수증을 자동 인식하고 조직 예산을 효율적으로 관리하는 PWA 개발

  - ### 필요성
  - 수기 입력의 번거로움 해소
  - 실시간 예산 추적 및 관리
  - 조직 재정 운영의 투명성 확보
  - 모바일/PC 크로스 플랫폼 접근성 향상

## 프로젝트 내용
  - ### 주요 기능
  **1. OCR 기반 영수증 자동 인식**
  - Azure Document Intelligence API를 활용한 영수증 이미지 자동 분석
  - 날짜, 금액, 가맹점명, 주소, 전화번호 자동 추출
  - AI 기반 자동 카테고리 분류 (9개 카테고리: 식비, 사무용품, 회식, 교통비, 공과금, 유흥, 교육, 의료, 기타)

  **2. 예산 관리 시스템**
  - 부서/조직별 예산 설정 및 관리
  - 실시간 예산 집행 현황 모니터링
  - 예산 대비 실제 지출 비교 분석
  - 카테고리별 예산 배분 및 추적

  **3. 다중 사용자 지원**
  - JWT 기반 사용자 인증 시스템
  - 역할 기반 접근 제어 (관리자/일반 사용자)
  - 부서별 사용자 할당 및 권한 관리

  **4. 리포트 및 분석**
  - Chart.js 기반 시각화 대시보드
  - 카테고리별 지출 분석
  - PDF 리포트 자동 생성 및 다운로드
  - 기간별 필터링 및 맞춤 리포트

  **5. PWA 기능**
  - 서비스 워커 기반 오프라인 지원
  - 모바일/PC 앱 설치 가능
  - 자동 업데이트 메커니즘
  - 반응형 디자인 (모바일 우선)

  - ### 기대 효과
  - **업무 효율성 증대**: OCR 자동 인식으로 수기 입력 시간 90% 단축
  - **실시간 예산 관리**: 즉각적인 예산 현황 파악 및 의사결정 지원
  - **투명한 재정 운영**: 모든 지출 내역의 실시간 추적 및 감사 가능
  - **접근성 향상**: PWA 기술로 모바일/PC 어디서나 사용 가능

## 기술 스택

  ### 💻 Frontend
  ![Vue.js](https://img.shields.io/badge/Vue.js_3-4FC08D?style=for-the-badge&logo=vuedotjs&logoColor=white)
  ![Vite](https://img.shields.io/badge/Vite-646CFF?style=for-the-badge&logo=vite&logoColor=white)
  ![TailwindCSS](https://img.shields.io/badge/Tailwind_CSS-06B6D4?style=for-the-badge&logo=tailwindcss&logoColor=white)
  ![Pinia](https://img.shields.io/badge/Pinia-FFD859?style=for-the-badge&logo=pinia&logoColor=black)
  ![Chart.js](https://img.shields.io/badge/Chart.js-FF6384?style=for-the-badge&logo=chartdotjs&logoColor=white)

  ### 🔧 Backend
  ![Python](https://img.shields.io/badge/Python_3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
  ![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
  ![Uvicorn](https://img.shields.io/badge/Uvicorn-499848?style=for-the-badge&logo=gunicorn&logoColor=white)

  ### 💾 Database & Storage
  ![Firebase](https://img.shields.io/badge/Firebase_Firestore-FFCA28?style=for-the-badge&logo=firebase&logoColor=black)
  ![Firebase Storage](https://img.shields.io/badge/Firebase_Storage-FFCA28?style=for-the-badge&logo=firebase&logoColor=black)

  ### 🔍 OCR & AI
  ![Azure](https://img.shields.io/badge/Azure_Document_Intelligence-0078D4?style=for-the-badge&logo=microsoftazure&logoColor=white)
  ![OpenCV](https://img.shields.io/badge/OpenCV-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white)

  ### 🚀 Deployment
  ![Firebase Hosting](https://img.shields.io/badge/Firebase_Hosting-FFCA28?style=for-the-badge&logo=firebase&logoColor=black)
  ![AWS EC2](https://img.shields.io/badge/AWS_EC2-FF9900?style=for-the-badge&logo=amazonec2&logoColor=white)

## 프로젝트 구조

```
ossw-competition25-yee/
├── 002 Code/
│   ├── frontend/              # Vue.js 프론트엔드
│   │   ├── src/
│   │   │   ├── components/    # Vue 컴포넌트
│   │   │   ├── api/          # API 클라이언트 모듈
│   │   │   ├── services/     # 유틸리티 서비스
│   │   │   ├── assets/       # 정적 파일
│   │   │   ├── App.vue       # 루트 컴포넌트
│   │   │   └── main.js       # 진입점
│   │   ├── public/           # PWA 아이콘 & 매니페스트
│   │   ├── vite.config.js    # Vite 설정
│   │   └── package.json
│   │
│   └── backend/              # FastAPI 백엔드
│       ├── src/
│       │   ├── api/routes/   # API 엔드포인트
│       │   ├── core/         # 설정 & Firebase
│       │   ├── models/       # 데이터 모델
│       │   ├── schemas/      # Pydantic 스키마
│       │   ├── services/     # 비즈니스 로직
│       │   └── utils/        # 헬퍼 함수
│       ├── main.py           # FastAPI 앱 진입점
│       └── requirements.txt  # Python 의존성
│
├── README.md
└── .gitignore
```

## 주요 기술 특징

### 🎯 OCR 처리 파이프라인
1. 영수증 이미지 업로드 → Firebase Storage 저장
2. Azure Document Intelligence API 호출
3. 날짜, 금액, 가맹점 정보 자동 추출
4. AI 기반 카테고리 자동 분류
5. 사용자 확인 → Firestore 저장

### 🔐 보안
- JWT 토큰 기반 인증
- Bcrypt 비밀번호 해싱
- Firebase 보안 규칙
- CORS 미들웨어 설정
- Pydantic 입력 검증

### ⚡ 성능 최적화
- Vite 번들링 & 코드 스플리팅
- 서비스 워커 캐싱
- CV2/Pillow 이미지 압축
- Firestore 인덱싱
- FastAPI 비동기 처리

## 라이선스
MIT License

## 문의
프로젝트 관련 문의사항은 팀원에게 연락 바랍니다.