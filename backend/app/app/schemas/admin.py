from typing import Optional

from pydantic import BaseModel, EmailStr


# Shared properties
class AdminBase(BaseModel):
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = True
    full_name: Optional[str] = None


class AdminBaseInDB(AdminBase):
    id: int = None

    class Config:
        orm_mode = True


# Properties to receive via API on creation
class AdminCreate(AdminBaseInDB):
    email: EmailStr
    password: str


# Properties to receive via API on update
class AdminUpdate(AdminBaseInDB):
    password: Optional[str] = None


# Additional properties to return via API
class Admin(AdminBaseInDB):
    pass


# Additional properties stored in DB
class AdminInDB(AdminBaseInDB):
    hashed_password: str
