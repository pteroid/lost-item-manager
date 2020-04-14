from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import DatabaseError, IntegrityError
from sqlalchemy.orm import Session

from app import crud
from app.api.utils.db import get_db
from app.api.utils.security import get_current_active_admin
from app.models.admin import Admin as DBUser
from app.schemas.item import Item, ItemCreate, ItemUpdate

router = APIRouter()


@router.get("/", response_model=List[Item])
def read_items(
        db: Session = Depends(get_db),
        skip: int = 0,
        limit: int = 100
):
    """
    Retrieve items.
    """
    items = crud.item.get_multi(db, skip=skip, limit=limit)
    return items


@router.post("/", response_model=Item)
def create_item(
        *,
        db: Session = Depends(get_db),
        item_in: ItemCreate,
        current_user: DBUser = Depends(get_current_active_admin),
):
    """
    Create new item.
    """
    try:
        item = crud.item.create(db_session=db, obj_in=item_in)
    except IntegrityError as e:
        raise HTTPException(status_code=406, detail=str(e.orig))
    return item


@router.put("/{id}", response_model=Item)
def update_item(
        *,
        db: Session = Depends(get_db),
        id: int,
        item_in: ItemUpdate,
        current_user: DBUser = Depends(get_current_active_admin),
):
    """
    Update an item.
    """
    item = crud.item.get(db_session=db, id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    try:
        item = crud.item.update(db_session=db, db_obj=item, obj_in=item_in)
    except IntegrityError as e:
        raise HTTPException(status_code=406, detail=str(e.orig))
    return item


@router.get("/{id}", response_model=Item)
def read_item(
        *,
        db: Session = Depends(get_db),
        id: int,
):
    """
    Get item by ID.
    """
    item = crud.item.get(db_session=db, id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.delete("/{id}", response_model=Item)
def delete_item(
        *,
        db: Session = Depends(get_db),
        id: int,
        current_user: DBUser = Depends(get_current_active_admin),
):
    """
    Delete an item.
    """
    item = crud.item.get(db_session=db, id=id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    item = crud.item.remove(db_session=db, id=id)
    return item
