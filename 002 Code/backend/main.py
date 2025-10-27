from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.core.config import settings
from src.api.routes import budget, receipt, auth, expense, department, admin

# FastAPI 앱 초기화
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="NAVER Clover OCR을 활용한 조직예산 관리 API",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 또는 ["http://ec2-43-203-136-37.ap-northeast-2.compute.amazonaws.com:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록 - prefix는 각 라우터에 이미 정의되어 있음
app.include_router(auth.router)
app.include_router(budget.router)
app.include_router(receipt.router)
app.include_router(expense.router)
app.include_router(department.router)
app.include_router(admin.router)


@app.get("/")
async def root():
    """API 루트 엔드포인트"""
    return {
        "message": "Budget Management API",
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health")
async def health_check():
    """헬스 체크 엔드포인트"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
