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
        """
        사용자 회원가입

        Args:
            user_data: 사용자 정보 (email, password, name)

        Returns:
            생성된 사용자 정보

        Raises:
            Exception: 이메일 중복 또는 생성 실패
        """
        try:
            email = user_data["email"]
            password = user_data["password"]
            name = user_data.get("name", "")

            # 1. 이메일 중복 체크
            existing_users = self.db.collection(self.collection)\
                .where("email", "==", email)\
                .limit(1)\
                .stream()

            if any(existing_users):
                raise Exception("이미 존재하는 이메일입니다")

            # 2. 비밀번호 해싱
            hashed_password = self.get_password_hash(password)

            # 3. Firestore에 사용자 저장
            user_doc = {
                "email": email,
                "name": name,
                "hashed_password": hashed_password,
                "role": "user",
                "is_active": True,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }

            doc_ref = self.db.collection(self.collection).document()
            doc_ref.set(user_doc)

            # 4. 응답 데이터 생성 (비밀번호 제외)
            user_doc["id"] = doc_ref.id
            del user_doc["hashed_password"]

            return user_doc

        except Exception as e:
            raise Exception(f"회원가입 실패: {str(e)}")

    async def login(self, email: str, password: str) -> Dict[str, Any]:
        """
        사용자 로그인

        Args:
            email: 사용자 이메일
            password: 비밀번호

        Returns:
            액세스 토큰과 사용자 정보

        Raises:
            Exception: 이메일/비밀번호 불일치 또는 계정 비활성화
        """
        try:
            # 1. Firestore에서 사용자 조회
            users = self.db.collection(self.collection)\
                .where("email", "==", email)\
                .limit(1)\
                .stream()

            user_doc = None
            user_id = None

            for doc in users:
                user_doc = doc.to_dict()
                user_id = doc.id
                break

            if not user_doc:
                raise Exception("이메일 또는 비밀번호가 일치하지 않습니다")

            # 2. 계정 활성화 상태 확인
            if not user_doc.get("is_active", True):
                raise Exception("비활성화된 계정입니다")

            # 3. 비밀번호 검증
            if not self.verify_password(password, user_doc["hashed_password"]):
                raise Exception("이메일 또는 비밀번호가 일치하지 않습니다")

            # 4. JWT 토큰 생성
            access_token = self.create_access_token({
                "sub": user_id,  # user_id를 sub에 저장
                "email": email,
                "role": user_doc.get("role", "user")
            })

            # 5. 응답 데이터 생성
            return {
                "access_token": access_token,
                "token_type": "bearer",
                "user": {
                    "id": user_id,
                    "email": email,
                    "name": user_doc.get("name", ""),
                    "role": user_doc.get("role", "user")
                }
            }

        except Exception as e:
            raise Exception(f"로그인 실패: {str(e)}")


auth_service = AuthService()
