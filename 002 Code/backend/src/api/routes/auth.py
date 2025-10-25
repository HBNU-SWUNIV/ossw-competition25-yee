from fastapi import APIRouter, HTTPException, Depends

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register")
async def register():
    """사용자 회원가입"""
    return {"message": "회원가입"}


@router.post("/login")
async def login():
    """사용자 로그인"""
    return {"message": "로그인"}


@router.post("/logout")
async def logout():
    """사용자 로그아웃"""
    return {"message": "로그아웃"}


@router.get("/me")
async def get_current_user():
    """현재 로그인한 사용자 정보 조회"""
    return {"message": "현재 사용자 정보"}
