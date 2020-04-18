from typing import List

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic.networks import EmailStr
from sqlalchemy.orm import Session

from app import crud
from app.api.utils.db import get_db
from app.api.utils.security import get_current_active_admin
from app.core import config
from app.models.admin import Admin as DBAdmin
from app.schemas.admin import Admin, AdminCreate, AdminUpdate
from app.utils import send_new_account_email

router = APIRouter()


@router.get("/", response_model=List[Admin])
def read_admins(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_admin: DBAdmin = Depends(get_current_active_admin),
):
    """
    Retrieve admins.
    """
    admins = crud.admin.get_multi(db, skip=skip, limit=limit)
    return admins


@router.post("/", response_model=Admin)
def create_admin(
    *,
    db: Session = Depends(get_db),
    admin_in: AdminCreate,
    current_admin: DBAdmin = Depends(get_current_active_admin),
):
    """
    Create new admin.
    """
    admin = crud.admin.get_by_email(db, email=admin_in.email)
    if admin:
        raise HTTPException(
            status_code=400,
            detail="The admin with this username already exists in the system.",
        )
    admin = crud.admin.create(db, obj_in=admin_in)
    if config.EMAILS_ENABLED and admin_in.email:
        send_new_account_email(
            email_to=admin_in.email, username=admin_in.email, password=admin_in.password
        )
    return admin


@router.put("/me", response_model=Admin)
def update_current_admin(
    *,
    db: Session = Depends(get_db),
    password: str = Body(None),
    full_name: str = Body(None),
    email: EmailStr = Body(None),
    current_admin: DBAdmin = Depends(get_current_active_admin),
):
    """
    Update own admin.
    """
    current_admin_data = jsonable_encoder(current_admin)
    admin_in = AdminUpdate(**current_admin_data)
    if password is not None:
        admin_in.password = password
    if full_name is not None:
        admin_in.full_name = full_name
    if email is not None:
        admin_in.email = email
    admin = crud.admin.update(db, db_obj=current_admin, obj_in=admin_in)
    return admin


@router.get("/me", response_model=Admin)
def read_current_admin(
    db: Session = Depends(get_db),
    current_admin: DBAdmin = Depends(get_current_active_admin),
):
    """
    Get current admin.
    """
    return current_admin


@router.post("/open", response_model=Admin)
def create_opened_admin(
    *,
    db: Session = Depends(get_db),
    password: str = Body(...),
    email: EmailStr = Body(...),
    full_name: str = Body(None),
):
    """
    Create new admin without the need to be logged in.
    """
    if not config.USERS_OPEN_REGISTRATION:
        raise HTTPException(
            status_code=403,
            detail="Open admin registration is forbidden on this server",
        )
    admin = crud.admin.get_by_email(db, email=email)
    if admin:
        raise HTTPException(
            status_code=400,
            detail="The admin with this username already exists in the system",
        )
    admin_in = AdminCreate(password=password, email=email, full_name=full_name)
    admin = crud.admin.create(db, obj_in=admin_in)
    return admin


@router.get("/{admin_id}", response_model=Admin)
def read_admin_by_id(
    admin_id: int,
    current_admin: DBAdmin = Depends(get_current_active_admin),
    db: Session = Depends(get_db),
):
    """
    Get a specific admin by id.
    """
    admin = crud.admin.get(db, id=admin_id)
    if admin == current_admin:
        return admin
    if not crud.admin.is_superadmin(current_admin):
        raise HTTPException(
            status_code=400, detail="The admin doesn't have enough privileges"
        )
    return admin


@router.put("/{admin_id}", response_model=Admin)
def update_admin(
    *,
    db: Session = Depends(get_db),
    admin_id: int,
    admin_in: AdminUpdate,
    current_admin: DBAdmin = Depends(get_current_active_admin),
):
    """
    Update a admin.
    """
    admin = crud.admin.get(db, id=admin_id)
    if not admin:
        raise HTTPException(
            status_code=404,
            detail="The admin with this username does not exist in the system",
        )
    admin = crud.admin.update(db, db_obj=admin, obj_in=admin_in)
    return admin
