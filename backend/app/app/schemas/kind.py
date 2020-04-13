from pydantic import BaseModel
from typing import Optional
from datetime import date


# Shared properties
class KindBase(BaseModel):
    id: int
    name: str


# Properties to receive on kind creation
class KindCreate(KindBase):
    pass


# Properties to receive on kind update
class KindUpdate(KindBase):
    pass


# Properties shared by models stored in DB
class KindInDBBase(KindBase):
    class Config:
        orm_mode = True


# Properties to return to client
class Kind(KindInDBBase):
    pass


# Properties properties stored in DB
class KindInDB(KindInDBBase):
    pass
