from typing import List

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic.networks import EmailStr
from sqlalchemy.orm import Session

from app import crud
from app.api.utils.db import get_db
from app.api.utils.security import get_current_active_admin
from app.core import config
from app.models.admin import Admin as DBUser
from app.schemas.admin import Admin, AdminCreate, AdminUpdate
from app.utils import send_new_account_email

router = APIRouter()


@router.get("/", response_model=List[Admin])
def read_admins(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: DBUser = Depends(get_current_active_admin),
):
    """
    Retrieve users.
    """
    users = crud.admin.get_multi(db, skip=skip, limit=limit)
    return users


@router.post("/", response_model=Admin)
def create_admin(
    *,
    db: Session = Depends(get_db),
    user_in: AdminCreate,
    current_user: DBUser = Depends(get_current_active_admin),
):
    """
    Create new user.
    """
    user = crud.admin.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
    user = crud.admin.create(db, obj_in=user_in)
    if config.EMAILS_ENABLED and user_in.email:
        send_new_account_email(
            email_to=user_in.email, username=user_in.email, password=user_in.password
        )
    return user


@router.put("/me", response_model=Admin)
def update_user_me(
    *,
    db: Session = Depends(get_db),
    password: str = Body(None),
    full_name: str = Body(None),
    email: EmailStr = Body(None),
    current_user: DBUser = Depends(get_current_active_admin),
):
    """
    Update own user.
    """
    current_user_data = jsonable_encoder(current_user)
    user_in = AdminUpdate(**current_user_data)
    if password is not None:
        user_in.password = password
    if full_name is not None:
        user_in.full_name = full_name
    if email is not None:
        user_in.email = email
    user = crud.admin.update(db, db_obj=current_user, obj_in=user_in)
    return user


@router.get("/me", response_model=Admin)
def read_user_me(
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(get_current_active_admin),
):
    """
    Get current user.
    """
    return current_user


@router.post("/open", response_model=Admin)
def create_user_open(
    *,
    db: Session = Depends(get_db),
    password: str = Body(...),
    email: EmailStr = Body(...),
    full_name: str = Body(None),
):
    """
    Create new user without the need to be logged in.
    """
    if not config.USERS_OPEN_REGISTRATION:
        raise HTTPException(
            status_code=403,
            detail="Open user registration is forbidden on this server",
        )
    user = crud.admin.get_by_email(db, email=email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system",
        )
    user_in = AdminCreate(password=password, email=email, full_name=full_name)
    user = crud.admin.create(db, obj_in=user_in)
    return user


@router.get("/{user_id}", response_model=Admin)
def read_user_by_id(
    user_id: int,
    current_user: DBUser = Depends(get_current_active_admin),
    db: Session = Depends(get_db),
):
    """
    Get a specific user by id.
    """
    user = crud.admin.get(db, id=user_id)
    if user == current_user:
        return user
    if not crud.admin.is_superuser(current_user):
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return user


@router.put("/{user_id}", response_model=Admin)
def update_user(
    *,
    db: Session = Depends(get_db),
    user_id: int,
    user_in: AdminUpdate,
    current_user: DBUser = Depends(get_current_active_admin),
):
    """
    Update a user.
    """
    user = crud.admin.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system",
        )
    user = crud.admin.update(db, db_obj=user, obj_in=user_in)
    return user
