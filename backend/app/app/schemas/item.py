from pydantic import BaseModel
from typing import Optional
from datetime import date


# Shared properties
class ItemBase(BaseModel):
    id: int
    picked_at: date
    place_id: int
    kind_id: int
    detail: Optional[str]


# Properties to receive on item creation
class ItemCreate(ItemBase):
    pass


# Properties to receive on item update
class ItemUpdate(ItemBase):
    pass


# Properties shared by models stored in DB
class ItemInDBBase(ItemBase):
    class Config:
        orm_mode = True


# Properties to return to client
class Item(ItemInDBBase):
    pass


# Properties properties stored in DB
class ItemInDB(ItemInDBBase):
    pass
