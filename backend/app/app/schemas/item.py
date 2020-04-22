from datetime import date
from typing import Optional

from pydantic import AnyUrl, BaseModel


# Shared properties
class ItemBase(BaseModel):
    picked_at: date
    place_id: int
    kind_id: int
    detail: Optional[str]
    image_url: Optional[AnyUrl]


# Properties to receive on item creation
class ItemCreate(ItemBase):
    pass


# Properties to receive on item update
class ItemUpdate(ItemBase):
    id: int


# Properties shared by models stored in DB
class ItemInDBBase(ItemBase):
    id: int

    class Config:
        orm_mode = True


# Properties to return to client
class Item(ItemInDBBase):
    pass


# Properties properties stored in DB
class ItemInDB(ItemInDBBase):
    pass
