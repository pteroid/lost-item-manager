from app.crud.base import CRUDBase
from app.models.kind import Kind
from app.schemas.kind import KindCreate, KindUpdate


class CRUDKind(CRUDBase[Kind, KindCreate, KindUpdate]):
    pass


kind = CRUDKind(Kind)
