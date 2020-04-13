from app.models.place import Place
from app.schemas.place import PlaceCreate, PlaceUpdate
from app.crud.base import CRUDBase


class CRUDPlace(CRUDBase[Place, PlaceCreate, PlaceUpdate]):
    pass


place = CRUDPlace(Place)
