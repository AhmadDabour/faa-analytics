from app.database import Base
from sqlalchemy import Column, Float, String, Date, ForeignKey

class Weather(Base):
    __tablename__ = "weather"
    airport_code = Column(String, ForeignKey("airports.iata_code"), primary_key=True)
    date = Column(Date, primary_key=True)
    rain = Column(Float)
    snow_depth = Column(Float)
    max_temp = Column(Float)
    min_temp = Column(Float)
    wind_speed = Column(Float) 