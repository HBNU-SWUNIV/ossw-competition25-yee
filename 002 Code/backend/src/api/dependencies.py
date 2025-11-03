from fastapi import Header, HTTPException, Depends
from typing import Dict, Any
from src.services.auth_service import auth_service


async def verify_token(authorization: str = Header(None)) -> str:
    """
    토큰 검증 의존성

    Args:
        authorization: Authorization 헤더 (Bearer {token})

    Returns:
        검증된 토큰 문자열

    Raises:
        HTTPException: 토큰이 없거나 유효하지 않은 경우
    """
    if not authorization:
        raise HTTPException(status_code=401, detail="인증 토큰이 필요합니다")

    # Bearer 토큰 형식 확인
    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise HTTPException(
                status_code=401,
                detail="유효하지 않은 인증 스킴입니다. Bearer 토큰을 사용하세요"
            )
    except ValueError:
        raise HTTPException(
            status_code=401,
            detail="유효하지 않은 토큰 형식입니다"
        )

    # JWT 토큰 검증
    payload = auth_service.decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="유효하지 않거나 만료된 토큰입니다")

    return token


async def get_current_user(authorization: str = Header(None)) -> Dict[str, Any]:
    """
    현재 사용자 정보 가져오기

    Args:
        authorization: Authorization 헤더 (Bearer {token})

    Returns:
        사용자 정보 딕셔너리 (user_id, email, role)

    Raises:
        HTTPException: 토큰이 없거나 유효하지 않은 경우
    """
    # 토큰 검증
    token = await verify_token(authorization)

    # 토큰에서 사용자 정보 추출
    payload = auth_service.decode_token(token)

    if not payload or "sub" not in payload:
        raise HTTPException(status_code=401, detail="유효하지 않은 토큰입니다")

    return {
        "user_id": payload["sub"],
        "email": payload.get("email"),
        "role": payload.get("role", "user"),
        "organizationName": payload.get("organizationName"),
        "organizationType": payload.get("organizationType"),
        "school": payload.get("school"),
        "department": payload.get("department")
    }
