from app.database import Base
from sqlalchemy import ForeignKey, Column, String, Date, Integer, Float, Boolean

class Flight(Base):
    __tablename__ = "flights"
    
    id = Column(Integer, primary_key=True, autoincrement= True)
    date = Column(Date, index=True)
    airline_code = Column(String(2), ForeignKey("airlines.iata_code"), nullable = False, index=True) # Connects flight and airline tables, where flights uses airline codes
    origin_airport = Column(String(3), ForeignKey("airports.iata_code"), nullable = False, index=True) # Connects flights and routes, where flights uses the origin airport code
    dest_airport = Column(String(3), ForeignKey("airports.iata_code"), nullable=False, index=True) # Connects flights and routes, where flights uses the destination airport code
    flight_number = Column(Integer)
    scheduled_dep_time = Column(Integer)
    actual_dep_time = Column(Integer)
    dep_delay = Column(Float, nullable=True)
    dep_delay_15 = Column(Boolean) # Departed >= 15 minutes late
    arr_time = Column(Integer)
    scheduled_arr_time = Column(Integer)
    arr_delay = Column(Float, nullable=True)
    arr_delay_15 = Column(Boolean) # Arrived >= 15 minutes late
    cancelled = Column(Boolean)
    cancellation_code = Column(String(1), nullable=True)
    diverted = Column(Boolean)
    scheduled_elapsed_time = Column(Integer)
    actual_elapsed_time = Column(Integer) # Includes Taxi arrival time
    air_time = Column(Integer) # Time spent in air
    distance = Column(Integer)
    carrier_delay = Column(Float, nullable=True) # Delays caused by airlines
    weather_delay = Column(Float, nullable=True) # Delays cuased by weather complications
    nas_delay = Column(Float, nullable=True) # Delays caused by air traffic control (FAA responsibility)
    security_delay = Column(Float, nullable=True)
    late_aircraft_delay = Column(Float, nullable=True)
    