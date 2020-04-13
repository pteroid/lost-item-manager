from app.models.item import Item
from app.schemas.item import ItemCreate, ItemUpdate
from app.crud.base import CRUDBase


class CRUDItem(CRUDBase[Item, ItemCreate, ItemUpdate]):
    pass


item = CRUDItem(Item)
