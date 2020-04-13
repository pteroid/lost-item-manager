from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud
from app.api.utils.db import get_db
from app.api.utils.security import get_current_active_admin
from app.models.admin import Admin as DBUser
from app.schemas.kind import Kind, KindCreate, KindUpdate

router = APIRouter()


@router.get("/", response_model=List[Kind])
def read_kinds(
        db: Session = Depends(get_db),
        skip: int = 0,
        limit: int = 100
):
    """
    Retrieve kinds.
    """
    kinds = crud.kind.get_multi(db, skip=skip, limit=limit)
    return kinds


@router.post("/", response_model=Kind)
def create_kind(
        *,
        db: Session = Depends(get_db),
        kind_in: KindCreate,
        current_user: DBUser = Depends(get_current_active_admin),
):
    """
    Create new kind.
    """
    kind = crud.kind.create(
        db_session=db, obj_in=kind_in
    )
    return kind


@router.put("/{id}", response_model=Kind)
def update_kind(
        *,
        db: Session = Depends(get_db),
        id: int,
        kind_in: KindUpdate,
        current_user: DBUser = Depends(get_current_active_admin),
):
    """
    Update an kind.
    """
    kind = crud.kind.get(db_session=db, id=id)
    if not kind:
        raise HTTPException(status_code=404, detail="Kind not found")
    kind = crud.kind.update(db_session=db, db_obj=kind, obj_in=kind_in)
    return kind


@router.get("/{id}", response_model=Kind)
def read_kind(
        *,
        db: Session = Depends(get_db),
        id: int,
):
    """
    Get kind by ID.
    """
    kind = crud.kind.get(db_session=db, id=id)
    if not kind:
        raise HTTPException(status_code=404, detail="Kind not found")
    return kind


@router.delete("/{id}", response_model=Kind)
def delete_kind(
        *,
        db: Session = Depends(get_db),
        id: int,
        current_user: DBUser = Depends(get_current_active_admin),
):
    """
    Delete an kind.
    """
    kind = crud.kind.get(db_session=db, id=id)
    if not kind:
        raise HTTPException(status_code=404, detail="Kind not found")
    kind = crud.kind.remove(db_session=db, id=id)
    return kind
