from app.database import Base
from sqlalchemy import Column, String, Float
class Airport(Base):
    __tablename__ = "airports"

    iata_code = Column(String(3), primary_key=True)
    city = Column(String(100), nullable= True)
    state = Column(String(2), nullable = True)
    latitude = Column(Float)
    longitude = Column(Float)
    noaa_station_id = Column(String(100))