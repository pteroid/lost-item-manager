from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Place(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    items = relationship("Item")
