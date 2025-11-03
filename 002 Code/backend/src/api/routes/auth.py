from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Optional
from src.schemas.user import UserCreate, UserLogin, UserResponse, TokenResponse
from src.services.auth_service import auth_service
from src.api.dependencies import get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserResponse)
async def register(user_data: UserCreate):
    """
    사용자 회원가입

    - 이메일 중복 체크
    - 비밀번호 해싱 후 저장
    - Firestore에 사용자 정보 저장
    """
    try:
        user = await auth_service.register_user(user_data.dict())
        return user
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login", response_model=TokenResponse)
async def login(credentials: UserLogin):
    """
    사용자 로그인

    - 이메일/비밀번호 검증
    - JWT 액세스 토큰 발급
    """
    try:
        result = await auth_service.login(
            email=credentials.email,
            password=credentials.password
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))


@router.post("/logout")
async def logout():
    """
    사용자 로그아웃

    Note: JWT 토큰은 stateless이므로 서버에서 무효화 불가
    클라이언트에서 토큰을 삭제하면 됨
    """
    return {"message": "로그아웃 성공"}


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: dict = Depends(get_current_user)):
    """
    현재 로그인한 사용자 정보 조회

    - JWT 토큰에서 사용자 정보 추출
    - Authorization 헤더 필요: Bearer {token}
    """
    try:
        # Firestore에서 전체 사용자 정보 가져오기
        user = await auth_service.get_user_by_id(current_user["user_id"])
        if not user:
            raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다")
        return user
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/users/organization")
async def get_users_by_organization(
    organizationName: str = Query(..., description="조직 이름"),
    current_user: dict = Depends(get_current_user)
):
    """
    특정 자치기구의 모든 사용자 조회

    - 같은 자치기구의 임원 정보 조회
    - Authorization 헤더 필요: Bearer {token}
    """
    try:
        users = await auth_service.get_users_by_organization(organizationName)
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/users/all-organizations")
async def get_all_organizations(current_user: dict = Depends(get_current_user)):
    """
    모든 자치기구 목록 조회

    - 각 자치기구의 임원 정보 포함
    - Authorization 헤더 필요: Bearer {token}
    """
    try:
        organizations = await auth_service.get_all_organizations()
        return organizations
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
