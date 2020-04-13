from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud
from app.api.utils.db import get_db
from app.api.utils.security import get_current_active_admin
from app.models.admin import Admin as DBUser
from app.schemas.place import Place, PlaceCreate, PlaceUpdate

router = APIRouter()


@router.get("/", response_model=List[Place])
def read_places(
        db: Session = Depends(get_db),
        skip: int = 0,
        limit: int = 100
):
    """
    Retrieve places.
    """
    places = crud.place.get_multi(db, skip=skip, limit=limit)
    return places


@router.post("/", response_model=Place)
def create_place(
        *,
        db: Session = Depends(get_db),
        place_in: PlaceCreate,
        current_user: DBUser = Depends(get_current_active_admin),
):
    """
    Create new place.
    """
    place = crud.place.create(
        db_session=db, obj_in=place_in
    )
    return place


@router.put("/{id}", response_model=Place)
def update_place(
        *,
        db: Session = Depends(get_db),
        id: int,
        place_in: PlaceUpdate,
        current_user: DBUser = Depends(get_current_active_admin),
):
    """
    Update an place.
    """
    place = crud.place.get(db_session=db, id=id)
    if not place:
        raise HTTPException(status_code=404, detail="Place not found")
    place = crud.place.update(db_session=db, db_obj=place, obj_in=place_in)
    return place


@router.get("/{id}", response_model=Place)
def read_place(
        *,
        db: Session = Depends(get_db),
        id: int,
):
    """
    Get place by ID.
    """
    place = crud.place.get(db_session=db, id=id)
    if not place:
        raise HTTPException(status_code=404, detail="Place not found")
    return place


@router.delete("/{id}", response_model=Place)
def delete_place(
        *,
        db: Session = Depends(get_db),
        id: int,
        current_user: DBUser = Depends(get_current_active_admin),
):
    """
    Delete an place.
    """
    place = crud.place.get(db_session=db, id=id)
    if not place:
        raise HTTPException(status_code=404, detail="Place not found")
    place = crud.place.remove(db_session=db, id=id)
    return place
