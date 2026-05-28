import csv
import os
from app.database import SessionLocal
from app.models.airport import Airport
csv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "raw", "airports.csv")
db = SessionLocal()
with open (csv_path, 'r', encoding="utf8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        airport = db.query(Airport).filter(Airport.iata_code == row["code"]).first()
        if airport:
            airport.latitude = row["latitude"]
            airport.longitude = row["longitude"]
            db.commit()