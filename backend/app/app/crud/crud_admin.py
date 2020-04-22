from typing import Optional

from sqlalchemy.orm import Session

from app.core.security import get_password_hash, verify_password
from app.crud.base import CRUDBase
from app.models.admin import Admin
from app.schemas.admin import AdminCreate, AdminUpdate


class CRUDAdmin(CRUDBase[Admin, AdminCreate, AdminUpdate]):
    def get_by_email(self, db_session: Session, *, email: str) -> Optional[Admin]:
        return db_session.query(Admin).filter(Admin.email == email).first()

    def create(self, db_session: Session, *, obj_in: AdminCreate) -> Admin:
        db_obj = Admin(
            email=obj_in.email,
            hashed_password=get_password_hash(obj_in.password),
            full_name=obj_in.full_name,
        )
        db_session.add(db_obj)
        db_session.commit()
        db_session.refresh(db_obj)
        return db_obj

    def authenticate(
        self, db_session: Session, *, email: str, password: str
    ) -> Optional[Admin]:
        admin = self.get_by_email(db_session, email=email)
        if not admin:
            return None
        if not verify_password(password, admin.hashed_password):
            return None
        return admin

    def is_active(self, admin: Admin) -> bool:
        return admin.is_active


admin = CRUDAdmin(Admin)
