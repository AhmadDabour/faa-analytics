from app.database import SessionLocal
from app.models.flight import Flight
from app.models.weather import Weather
db = SessionLocal()
results = db.query(Flight, Weather).join(Weather, (Flight.origin_airport == Weather.airport_code) & (Flight.date == Weather.date)).limit(5).all()
print(results)
print(results[0][0].origin_airport)
print(results[0][1].max_temp)
result = db.query(Weather).filter(Weather.airport_code == "SFO", Weather.date == "2025-01-01").first()
print(result.max_temp, result.rain, result.snow_depth, result.min_temp, result.wind_speed)