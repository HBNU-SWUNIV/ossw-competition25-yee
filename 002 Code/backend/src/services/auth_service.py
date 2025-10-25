from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from jose import JWTError, jwt
from passlib.context import CryptContext
from src.core.config import settings
from src.core.firebase import firebase_client


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    """인증 서비스"""

    def __init__(self):
        self.db = firebase_client.db
        self.collection = "users"

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """비밀번호 검증"""
        return pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str) -> str:
        """비밀번호 해싱"""
        return pwd_context.hash(password)

    def create_access_token(self, data: dict) -> str:
        """JWT 액세스 토큰 생성"""
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=settings.JWT_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode,
            settings.JWT_SECRET_KEY,
            algorithm=settings.JWT_ALGORITHM
        )
        return encoded_jwt

    def decode_token(self, token: str) -> Optional[Dict[str, Any]]:
        """JWT 토큰 디코딩"""
        try:
            payload = jwt.decode(
                token,
                settings.JWT_SECRET_KEY,
                algorithms=[settings.JWT_ALGORITHM]
            )
            return payload
        except JWTError:
            return None

    async def register_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """사용자 회원가입"""
        try:
            # TODO: Firebase에 사용자 등록
            hashed_password = self.get_password_hash(user_data["password"])
            return {"id": "new_user_id", "email": user_data["email"]}
        except Exception as e:
            raise Exception(f"회원가입 실패: {str(e)}")

    async def login(self, email: str, password: str) -> Optional[str]:
        """사용자 로그인"""
        try:
            # TODO: Firebase에서 사용자 조회 및 비밀번호 검증
            # 임시 토큰 생성
            access_token = self.create_access_token({"sub": email})
            return access_token
        except Exception as e:
            raise Exception(f"로그인 실패: {str(e)}")


auth_service = AuthService()
