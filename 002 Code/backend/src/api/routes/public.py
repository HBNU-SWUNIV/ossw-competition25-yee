from fastapi import APIRouter, HTTPException, Depends, Query
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import uuid

from src.api.dependencies import get_current_user
from src.core.firebase import firebase_client


router = APIRouter(prefix="/public", tags=["public"])


@router.post("/share/create", response_model=Dict[str, Any])
async def create_share_link(current_user: Dict[str, Any] = Depends(get_current_user)):
    """
    자치기구관리 페이지 공유 토큰 생성 (로그인 필요)
    - 토큰은 Firestore의 public_shares 콜렉션에 저장
    - 기본 만료 7일
    """
    org_name = current_user.get("organizationName")
    if not org_name:
        raise HTTPException(status_code=400, detail="조직 정보가 없습니다")

    try:
        token = uuid.uuid4().hex
        expires_at = datetime.utcnow() + timedelta(days=7)

        doc = {
            "token": token,
            "organizationName": org_name,
            "created_at": datetime.utcnow(),
            "expires_at": expires_at,
            "active": True,
        }
        firebase_client.db.collection("public_shares").document(token).set(doc)
        return {"token": token, "expires_at": expires_at.isoformat()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def _validate_share_token(token: str) -> str:
    doc_ref = firebase_client.db.collection("public_shares").document(token)
    snap = doc_ref.get()
    if not snap.exists:
        raise HTTPException(status_code=404, detail="공유 토큰을 찾을 수 없습니다")
    data = snap.to_dict()
    if not data.get("active", True):
        raise HTTPException(status_code=403, detail="비활성화된 공유 링크입니다")
    expires_at = data.get("expires_at")
    if isinstance(expires_at, str):
        try:
            expires_at = datetime.fromisoformat(expires_at)
        except Exception:
            expires_at = None
    if expires_at and expires_at < datetime.utcnow():
        raise HTTPException(status_code=403, detail="공유 링크가 만료되었습니다")
    org_name = data.get("organizationName")
    if not org_name:
        raise HTTPException(status_code=400, detail="공유 데이터가 올바르지 않습니다")
    return org_name


@router.get("/organization", response_model=Dict[str, Any])
async def get_public_organization(token: str = Query(..., description="공유 토큰")):
    """
    공유 토큰 기반 자치기구 정보/임원 목록 조회 (무인증)
    """
    try:
        org_name = _validate_share_token(token)

        # users 컬렉션에서 해당 조직 사용자 조회
        users_ref = firebase_client.db.collection("users").where("organizationName", "==", org_name).stream()
        officers: List[Dict[str, Any]] = []
        org_meta: Dict[str, Any] = {
            "name": org_name,
            "organizationType": None,
            "organizationSubType": None,
            "school": None,
            "department": None,
            "officers": officers,
        }

        for doc in users_ref:
            u = doc.to_dict()
            officers.append({
                "id": doc.id,
                "name": u.get("name"),
                "position": u.get("position"),
                "email": u.get("email"),
            })
            # 메타는 최초 사용자 기준으로 채움
            if org_meta["organizationType"] is None:
                org_meta["organizationType"] = u.get("organizationType")
                org_meta["organizationSubType"] = u.get("organizationSubType")
                org_meta["school"] = u.get("school")
                org_meta["department"] = u.get("department")

        return org_meta
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/expenses", response_model=List[Dict[str, Any]])
async def get_public_expenses(
    token: str = Query(..., description="공유 토큰"),
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    limit: int = Query(1000, ge=1, le=10000),
):
    """
    공유 토큰 기반 조직 지출 목록 조회 (무인증, 읽기 전용)
    """
    try:
        org_name = _validate_share_token(token)

        # 같은 조직 사용자 ID 수집
        users_ref = firebase_client.db.collection("users").where("organizationName", "==", org_name).stream()
        user_ids = [u.id for u in users_ref]
        if not user_ids:
            return []

        # 모든 사용자 지출 모으기
        expenses: List[Dict[str, Any]] = []
        for uid in user_ids:
            q = firebase_client.db.collection("expenses").where("user_id", "==", uid)
            docs = q.stream()
            for d in docs:
                e = d.to_dict()
                e["id"] = d.id
                expenses.append(e)

        # Python에서 기간 필터, 정렬
        if start_date:
            expenses = [e for e in expenses if e.get("date") and e["date"] >= start_date]
        if end_date:
            expenses = [e for e in expenses if e.get("date") and e["date"] <= end_date]

        expenses.sort(key=lambda x: x.get("date", datetime.min), reverse=True)
        return expenses[:limit]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


