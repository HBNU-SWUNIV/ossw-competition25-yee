from fastapi import Header, HTTPException


async def verify_token(authorization: str = Header(None)):
    """토큰 검증 의존성"""
    if not authorization:
        raise HTTPException(status_code=401, detail="인증 토큰이 필요합니다")

    # TODO: JWT 토큰 검증 로직 구현
    return authorization


async def get_current_user(token: str = Header(None)):
    """현재 사용자 정보 가져오기"""
    # TODO: 토큰에서 사용자 정보 추출
    return {"user_id": "test_user"}
