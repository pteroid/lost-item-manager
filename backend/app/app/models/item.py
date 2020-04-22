from sqlalchemy import Column, Date, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Item(Base):
    id = Column(Integer, primary_key=True, index=True)
    picked_at = Column(Date)
    place_id = Column(Integer, ForeignKey("place.id"))
    kind_id = Column(Integer, ForeignKey("kind.id"))
    detail = Column(String)
    image_url = Column(String)

    place = relationship("Place")
    kind = relationship("Kind")
