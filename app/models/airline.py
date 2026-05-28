from app.database import Base
from sqlalchemy import Column, String

class Airline(Base):
    __tablename__ = "airlines"

    iata_code = Column(String(2), primary_key= True)
    name = Column(String(100), nullable=True)