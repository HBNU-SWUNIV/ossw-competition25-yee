import firebase_admin
from firebase_admin import credentials, firestore, auth
from src.core.config import settings


class FirebaseClient:
    """Firebase 클라이언트 싱글톤"""

    _instance = None
    _db = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        """Firebase 초기화"""
        try:
            # Firebase Admin SDK 초기화
            cred = credentials.Certificate({
                "type": "service_account",
                "project_id": settings.FIREBASE_PROJECT_ID,
                "private_key": settings.FIREBASE_PRIVATE_KEY,
                "client_email": settings.FIREBASE_CLIENT_EMAIL,
            })
            firebase_admin.initialize_app(cred)
            self._db = firestore.client()
            print("Firebase 초기화 성공")
        except Exception as e:
            print(f"Firebase 초기화 실패: {e}")

    @property
    def db(self):
        """Firestore 데이터베이스 인스턴스"""
        return self._db


# 싱글톤 인스턴스
firebase_client = FirebaseClient()
