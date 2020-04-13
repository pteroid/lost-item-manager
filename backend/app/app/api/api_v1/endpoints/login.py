from datetime import timedelta

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import crud
from app.api.utils.db import get_db
from app.api.utils.security import get_current_admin
from app.core import config
from app.core.jwt import create_access_token
from app.core.security import get_password_hash
from app.models.admin import Admin as DBUser
from app.schemas.msg import Msg
from app.schemas.token import Token
from app.schemas.admin import Admin
from app.utils import (
    generate_password_reset_token,
    send_reset_password_email,
    verify_password_reset_token,
)

router = APIRouter()


@router.post("/login/access-token", response_model=Token, tags=["login"])
def login_access_token(
    db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
):
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    admin = crud.admin.authenticate(
        db, email=form_data.username, password=form_data.password
    )
    if not admin:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not crud.admin.is_active(admin):
        raise HTTPException(status_code=400, detail="Inactive admin")
    access_token_expires = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": create_access_token(
            data={"user_id": admin.id}, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }


@router.post("/login/test-token", tags=["login"], response_model=Admin)
def test_token(current_admin: DBUser = Depends(get_current_admin)):
    """
    Test access token
    """
    return current_admin


@router.post("/password-recovery/{email}", tags=["login"], response_model=Msg)
def recover_password(email: str, db: Session = Depends(get_db)):
    """
    Password Recovery
    """
    admin = crud.admin.get_by_email(db, email=email)

    if not admin:
        raise HTTPException(
            status_code=404,
            detail="The admin with this username does not exist in the system.",
        )
    password_reset_token = generate_password_reset_token(email=email)
    send_reset_password_email(
        email_to=admin.email, email=email, token=password_reset_token
    )
    return {"msg": "Password recovery email sent"}


@router.post("/reset-password/", tags=["login"], response_model=Msg)
def reset_password(token: str = Body(...), new_password: str = Body(...), db: Session = Depends(get_db)):
    """
    Reset password
    """
    email = verify_password_reset_token(token)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid token")
    admin = crud.admin.get_by_email(db, email=email)
    if not admin:
        raise HTTPException(
            status_code=404,
            detail="The admin with this username does not exist in the system.",
        )
    elif not crud.admin.is_active(admin):
        raise HTTPException(status_code=400, detail="Inactive admin")
    hashed_password = get_password_hash(new_password)
    admin.hashed_password = hashed_password
    db.add(admin)
    db.commit()
    return {"msg": "Password updated successfully"}
