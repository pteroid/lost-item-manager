import jwt
from fastapi import Depends, HTTPException, Security
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError
from sqlalchemy.orm import Session
from starlette.status import HTTP_403_FORBIDDEN

from app import crud
from app.api.utils.db import get_db
from app.core import config
from app.core.jwt import ALGORITHM
from app.models.admin import Admin
from app.schemas.token import TokenPayload

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl="/api/v1/login/access-token")


def get_current_admin(
    db: Session = Depends(get_db), token: str = Security(reusable_oauth2)
):
    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=[ALGORITHM])
        token_data = TokenPayload(**payload)
    except PyJWTError:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials"
        )
    admin = crud.admin.get(db, id=token_data.user_id)
    if not admin:
        raise HTTPException(status_code=404, detail="Admin not found")
    return admin


def get_current_active_admin(current_user: Admin = Security(get_current_admin)):
    if not crud.admin.is_active(current_user):
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
