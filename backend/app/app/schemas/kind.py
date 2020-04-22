from pydantic import BaseModel


# Shared properties
class KindBase(BaseModel):
    id: int = None
    name: str


# Properties to receive on kind creation
class KindCreate(KindBase):
    pass


# Properties to receive on kind update
class KindUpdate(KindBase):
    id: int


# Properties shared by models stored in DB
class KindInDBBase(KindBase):
    id: int

    class Config:
        orm_mode = True


# Properties to return to client
class Kind(KindInDBBase):
    pass


# Properties properties stored in DB
class KindInDB(KindInDBBase):
    pass
