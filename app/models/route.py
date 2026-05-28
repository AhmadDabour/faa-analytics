from app.database import Base
from sqlalchemy import Column, String, ForeignKey

class Route(Base):
    __tablename__ = "routes"

    origin_code = Column(String(3), ForeignKey("airports.iata_code"), primary_key=True)
    dest_code = Column(String(3), ForeignKey("airports.iata_code"), primary_key= True)