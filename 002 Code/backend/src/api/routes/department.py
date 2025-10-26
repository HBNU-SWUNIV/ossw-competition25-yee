from fastapi import APIRouter, HTTPException, Depends
from typing import List
from src.schemas.department import DepartmentCreate, DepartmentUpdate, DepartmentResponse
from src.core.firebase import firebase_client
from src.api.dependencies import get_current_user
from datetime import datetime

# Firestore 데이터베이스 인스턴스
db = firebase_client.db

router = APIRouter(prefix="/department", tags=["department"])


@router.get("/", response_model=List[DepartmentResponse])
async def get_departments(current_user: dict = Depends(get_current_user)):
    """
    부서 목록 조회

    - 모든 부서 조회
    """
    try:
        departments_ref = db.collection("departments")
        docs = departments_ref.stream()

        departments = []
        for doc in docs:
            department_data = doc.to_dict()
            department_data["id"] = doc.id
            departments.append(department_data)

        return departments
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/", response_model=DepartmentResponse)
async def create_department(
    department_data: DepartmentCreate,
    current_user: dict = Depends(get_current_user)
):
    """
    부서 생성

    - name: 부서 이름
    - description: 부서 설명 (선택)
    - budget_limit: 예산 한도 (선택, 기본값: 0)
    - manager_id: 부서장 ID (선택)
    """
    try:
        # 관리자 권한 확인
        if current_user.get("role") != "admin":
            raise HTTPException(status_code=403, detail="부서 생성 권한이 없습니다")

        department_dict = department_data.dict()
        department_dict["created_at"] = datetime.now()
        department_dict["updated_at"] = datetime.now()

        # Firestore에 저장
        doc_ref = db.collection("departments").document()
        doc_ref.set(department_dict)

        # 생성된 부서 반환
        department_dict["id"] = doc_ref.id
        return department_dict
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{department_id}", response_model=DepartmentResponse)
async def get_department(
    department_id: str,
    current_user: dict = Depends(get_current_user)
):
    """특정 부서 조회"""
    try:
        doc_ref = db.collection("departments").document(department_id)
        doc = doc_ref.get()

        if not doc.exists:
            raise HTTPException(status_code=404, detail="부서를 찾을 수 없습니다")

        department_data = doc.to_dict()
        department_data["id"] = doc.id
        return department_data
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{department_id}", response_model=DepartmentResponse)
async def update_department(
    department_id: str,
    department_data: DepartmentUpdate,
    current_user: dict = Depends(get_current_user)
):
    """
    부서 수정

    - name, description, budget_limit, manager_id 수정 가능
    """
    try:
        # 관리자 권한 확인
        if current_user.get("role") != "admin":
            raise HTTPException(status_code=403, detail="부서 수정 권한이 없습니다")

        doc_ref = db.collection("departments").document(department_id)
        doc = doc_ref.get()

        if not doc.exists:
            raise HTTPException(status_code=404, detail="부서를 찾을 수 없습니다")

        # 수정할 데이터만 업데이트
        update_data = department_data.dict(exclude_unset=True)
        update_data["updated_at"] = datetime.now()

        doc_ref.update(update_data)

        # 수정된 부서 반환
        updated_doc = doc_ref.get()
        result = updated_doc.to_dict()
        result["id"] = updated_doc.id
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{department_id}")
async def delete_department(
    department_id: str,
    current_user: dict = Depends(get_current_user)
):
    """부서 삭제"""
    try:
        # 관리자 권한 확인
        if current_user.get("role") != "admin":
            raise HTTPException(status_code=403, detail="부서 삭제 권한이 없습니다")

        doc_ref = db.collection("departments").document(department_id)
        doc = doc_ref.get()

        if not doc.exists:
            raise HTTPException(status_code=404, detail="부서를 찾을 수 없습니다")

        doc_ref.delete()
        return {"message": "부서가 삭제되었습니다"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
