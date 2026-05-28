import requests
import os
from dotenv import load_dotenv
from app.database import SessionLocal
from app.models.airport import Airport
from app.models.weather import Weather
from datetime import datetime
load_dotenv()
NOAA_API_KEY = os.getenv("NOAA_API_KEY")
headers = {"token": NOAA_API_KEY}
data = requests.get("https://www.ncei.noaa.gov/cdo-web/api/v2/stations?datasetid=GHCND&sortfield=datacoverage&sortorder=desc&limit=5&extent=37.46,-122.51,37.82,-122.24&startdate=2025-01-01&enddate=2026-01-01", headers=headers)
print(data.json())