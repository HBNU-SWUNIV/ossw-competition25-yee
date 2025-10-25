from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """애플리케이션 설정"""

    # 앱 기본 설정
    APP_NAME: str = "Budget Management API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    # Firebase 설정
    FIREBASE_PROJECT_ID: Optional[str] = None
    FIREBASE_PRIVATE_KEY: Optional[str] = None
    FIREBASE_CLIENT_EMAIL: Optional[str] = None

    # NAVER Clover OCR 설정
    NAVER_OCR_API_URL: Optional[str] = None
    NAVER_OCR_SECRET_KEY: Optional[str] = None

    # CORS 설정
    ALLOWED_ORIGINS: list = [
        "http://localhost:3000",
        "http://localhost:8080",
        "http://localhost:5173",
    ]

    # JWT 설정
    JWT_SECRET_KEY: str = "your-secret-key-here-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 60 * 24  # 24시간

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
