import pytest
from app.models.airline import Airline
from app.models.airport import Airport
from app.models.flight import Flight
from app.models.weather import Weather
from app.database import SessionLocal
from sqlalchemy import text

@pytest.fixture(scope="session")
def ingestion():
    db = SessionLocal()
    new_airline = Airline(iata_code="AA", name="American Airlines")
    new_airport1 = Airport(
        iata_code="JFK",
        city="New York", state="NY",
        latitude=123.213, longitude=123.321,
        noaa_station_id="New York")
    new_airport2 = Airport(
        iata_code="LAX",
        city="Los Angeles", state="CA",
        latitude=123.456, longitude=123.222,
        noaa_station_id="Los Angeles")
    new_weather = Weather(
        airport_code="JFK", 
        date="2025-01-01", 
        rain=1.2, snow_depth=5.0, 
        max_temp=21.0, 
        min_temp=12.4, 
        wind_speed=7.5)
    flights = []
    for i in range(5):
        flights.append(Flight(
        date="2025-01-01",
        airline_code="AA",
        origin_airport="JFK",
        dest_airport="LAX",
        dep_delay_15=True,
        arr_delay_15=True,
        cancelled=True,
        cancellation_code="A",
        carrier_delay=30.0,
        weather_delay=10.0
    ))

    for f in flights:
        db.add(f)
    db.add(new_airline)
    db.add(new_airport1)
    db.add(new_airport2)
    db.add(new_weather)
    db.commit()
    yield
    db.execute(text("TRUNCATE flights, airlines, airports, weather CASCADE"))
    db.commit()
    db.close()
