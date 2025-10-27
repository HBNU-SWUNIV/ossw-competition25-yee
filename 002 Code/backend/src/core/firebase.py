import firebase_admin
from firebase_admin import credentials, firestore, auth, storage
from src.core.config import settings
from typing import Optional
import uuid
from datetime import timedelta


class FirebaseClient:
    """Firebase 클라이언트 싱글톤"""

    _instance = None
    _db = None
    _bucket = None

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
                "token_uri": "https://oauth2.googleapis.com/token",
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            })

            # Storage bucket 설정이 있는 경우 포함
            if settings.FIREBASE_STORAGE_BUCKET:
                firebase_admin.initialize_app(cred, {
                    'storageBucket': settings.FIREBASE_STORAGE_BUCKET
                })
                self._bucket = storage.bucket()
                print(f"Firebase Storage 초기화 성공: {settings.FIREBASE_STORAGE_BUCKET}")
            else:
                firebase_admin.initialize_app(cred)
                print("Firebase Storage bucket이 설정되지 않았습니다")

            self._db = firestore.client()
            print("Firebase 초기화 성공")
        except Exception as e:
            print(f"Firebase 초기화 실패: {e}")

    @property
    def db(self):
        """Firestore 데이터베이스 인스턴스"""
        return self._db

    @property
    def bucket(self):
        """Firebase Storage bucket 인스턴스"""
        return self._bucket

    def upload_image(self, image_data: bytes, user_id: str, filename: str = None) -> Optional[str]:
        """
        이미지를 Firebase Storage에 업로드하고 다운로드 URL 반환

        Args:
            image_data: 이미지 바이트 데이터
            user_id: 사용자 ID
            filename: 파일명 (선택, 지정하지 않으면 UUID 생성)

        Returns:
            다운로드 URL 또는 None
        """
        if not self._bucket:
            print("[Storage] Firebase Storage bucket이 설정되지 않았습니다")
            return None

        try:
            # 파일명 생성
            if not filename:
                filename = f"{uuid.uuid4()}.jpg"

            # 저장 경로: receipts/{user_id}/{filename}
            blob_path = f"receipts/{user_id}/{filename}"
            blob = self._bucket.blob(blob_path)

            # 이미지 업로드
            blob.upload_from_string(
                image_data,
                content_type='image/jpeg'
            )

            # 공개 URL 생성 (7일 만료)
            blob.make_public()
            download_url = blob.public_url

            print(f"[Storage] 이미지 업로드 성공: {blob_path}")
            return download_url

        except Exception as e:
            print(f"[Storage] 이미지 업로드 실패: {e}")
            return None

    def delete_image(self, image_url: str) -> bool:
        """
        Firebase Storage에서 이미지 삭제

        Args:
            image_url: 이미지 URL

        Returns:
            성공 여부
        """
        if not self._bucket:
            return False

        try:
            # URL에서 blob 경로 추출
            # 예: https://storage.googleapis.com/bucket-name/receipts/user_id/filename.jpg
            if "receipts/" in image_url:
                blob_path = image_url.split("receipts/")[1]
                blob_path = f"receipts/{blob_path}"
                blob = self._bucket.blob(blob_path)
                blob.delete()
                print(f"[Storage] 이미지 삭제 성공: {blob_path}")
                return True
        except Exception as e:
            print(f"[Storage] 이미지 삭제 실패: {e}")

        return False


# 싱글톤 인스턴스
firebase_client = FirebaseClient()
