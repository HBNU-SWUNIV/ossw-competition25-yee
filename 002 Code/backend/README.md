# Backend - FastAPI

## 백엔드 프로젝트

### 기술 스택
- **프레임워크**: Python 3.11+ / FastAPI 0.109.0
- **데이터베이스**: Firebase Firestore
- **인증**: JWT (JSON Web Token)
- **OCR**: PaddleOCR (오픈소스)
- **배포**: AWS EC2

### 설치 방법

#### 1. Python 가상환경 생성 및 활성화
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

#### 2. 의존성 설치
```bash
pip install -r requirements.txt
```

#### 3. 환경 변수 설정
```bash
# .env.example을 복사하여 .env 파일 생성
cp .env.example .env

# .env 파일을 열어 필요한 값들을 설정
# - Firebase 프로젝트 정보
# - JWT 시크릿 키
# (주의: PaddleOCR은 API 키가 필요 없습니다)
```

#### 4. 개발 서버 실행
```bash
# 방법 1: uvicorn 직접 실행
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# 방법 2: Python으로 실행
python main.py
```

서버가 실행되면 다음 주소에서 확인할 수 있습니다:
- API 문서 (Swagger): http://localhost:8000/docs
- API 문서 (ReDoc): http://localhost:8000/redoc
- API 루트: http://localhost:8000

### 프로젝트 구조
```
backend/
├── src/
│   ├── api/
│   │   ├── routes/              # API 라우트
│   │   │   ├── auth.py         # 인증 API
│   │   │   ├── budget.py       # 예산 관리 API
│   │   │   └── receipt.py      # 영수증 OCR API
│   │   └── dependencies.py      # 의존성 (인증 등)
│   ├── core/
│   │   ├── config.py           # 설정 관리
│   │   └── firebase.py         # Firebase 연결
│   ├── models/                  # 데이터 모델
│   │   ├── budget.py
│   │   ├── receipt.py
│   │   └── user.py
│   ├── schemas/                 # Pydantic 스키마
│   │   ├── budget.py
│   │   ├── receipt.py
│   │   └── user.py
│   ├── services/                # 비즈니스 로직
│   │   ├── auth_service.py
│   │   ├── budget_service.py
│   │   └── ocr_service.py
│   └── utils/                   # 유틸리티
│       └── helpers.py
├── tests/                       # 테스트 코드
├── .env.example                 # 환경 변수 예시
├── .gitignore
├── main.py                      # FastAPI 앱 엔트리포인트
├── requirements.txt             # Python 의존성
└── README.md
```

### API 엔드포인트

#### 인증 (Auth)
- `POST /api/auth/register` - 회원가입
- `POST /api/auth/login` - 로그인
- `POST /api/auth/logout` - 로그아웃
- `GET /api/auth/me` - 현재 사용자 정보

#### 예산 관리 (Budget)
- `GET /api/budget/` - 예산 목록 조회
- `POST /api/budget/` - 예산 생성
- `GET /api/budget/{budget_id}` - 특정 예산 조회
- `PUT /api/budget/{budget_id}` - 예산 수정
- `DELETE /api/budget/{budget_id}` - 예산 삭제

#### 영수증 (Receipt)
- `POST /api/receipt/upload` - 영수증 업로드 및 OCR 처리
- `GET /api/receipt/` - 영수증 목록 조회
- `GET /api/receipt/{receipt_id}` - 특정 영수증 조회
- `PUT /api/receipt/{receipt_id}` - 영수증 정보 수정
- `DELETE /api/receipt/{receipt_id}` - 영수증 삭제

#### 기타
- `GET /` - API 정보
- `GET /health` - 헬스 체크

### 개발 가이드

#### 새로운 API 추가하기
1. `src/api/routes/`에 새 라우터 파일 생성
2. `src/schemas/`에 요청/응답 스키마 정의
3. `src/services/`에 비즈니스 로직 구현
4. `main.py`에 라우터 등록

#### 테스트 실행
```bash
pytest
```

### 주의사항
- 다른 Open Source SW를 사용하는 경우 저작권을 명시해야 함
- 특정 기업의 기밀 정보 또는 개인 정보 등의 데이터는 제외할 것
- `.env` 파일은 절대 Git에 커밋하지 말 것
- Firebase 서비스 계정 키는 안전하게 관리할 것

### Open Source 라이선스
이 프로젝트에서 사용하는 주요 오픈소스:
- **FastAPI**: MIT License
- **Firebase Admin SDK**: Apache License 2.0
- **Pydantic**: MIT License
- **Uvicorn**: BSD License
- **PaddleOCR**: Apache License 2.0
- **PaddlePaddle**: Apache License 2.0

### OCR 기능
이 프로젝트는 영수증 인식을 위해 **PaddleOCR** (오픈소스)을 사용합니다.

#### PaddleOCR 특징
- **완전 오픈소스**: Apache 2.0 라이선스
- **API 키 불필요**: 로컬에서 직접 실행
- **한글 지원 우수**: 한국어 영수증 인식 가능
- **자동 영수증 파싱**: 상호명, 날짜, 금액, 품목 자동 추출

#### 첫 실행 시 주의사항
첫 실행 시 PaddleOCR이 한글 모델을 자동으로 다운로드합니다 (~100MB).
네트워크 연결이 필요하며, 다운로드는 한 번만 수행됩니다.
