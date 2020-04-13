from pydantic import BaseModel
from typing import Optional
from datetime import date


# Shared properties
class PlaceBase(BaseModel):
    id: int = None
    name: str


# Properties to receive on place creation
class PlaceCreate(PlaceBase):
    pass


# Properties to receive on place update
class PlaceUpdate(PlaceBase):
    id: int


# Properties shared by models stored in DB
class PlaceInDBBase(PlaceBase):
    id: int

    class Config:
        orm_mode = True


# Properties to return to client
class Place(PlaceInDBBase):
    pass


# Properties properties stored in DB
class PlaceInDB(PlaceInDBBase):
    pass
