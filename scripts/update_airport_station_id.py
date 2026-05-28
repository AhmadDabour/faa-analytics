import requests
from app.database import SessionLocal
from app.models.airport import Airport
from app.models.weather import Weather
import os
from dotenv import load_dotenv
load_dotenv()
NOAA_API_KEY = os.getenv("NOAA_API_KEY")
headers = {"token": NOAA_API_KEY}
db = SessionLocal()
info = db.query(Airport).all()
weather = {row.airport_code for row in db.query(Weather.airport_code).distinct()}
counter = 0
for row in info:
    found = False
    lat = row.latitude
    long = row.longitude
    min_lat = lat - 0.5
    min_long = long - 0.5
    max_lat = lat + 0.5
    max_long = long + 0.5
    result = requests.get(f"https://www.ncei.noaa.gov/cdo-web/api/v2/stations?datasetid=GHCND&sortfield=datacoverage&sortorder=desc&limit=5&extent={min_lat},{min_long},{max_lat},{max_long}&startdate=2025-01-01&enddate=2026-02-01", headers=headers)
    print(result.status_code)
    data = result.json()
    if "USW" not in row.noaa_station_id:
        for i in data["results"]:
            if "USW" in i["id"]:
                row.noaa_station_id = i["id"]
                found = True
                break
        if data.get("results") and data["results"][0]["maxdate"] >= "2025-01-01" and not found:
            row.noaa_station_id = data["results"][0]["id"]
            counter += 1
db.commit()
print(counter)
    