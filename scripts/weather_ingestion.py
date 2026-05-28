import requests
import os
from dotenv import load_dotenv
from app.database import SessionLocal
from app.models.airport import Airport
from app.models.weather import Weather
from datetime import datetime
data_url = "https://www.ncei.noaa.gov/cdo-web/api/v2/data"
load_dotenv()
NOAA_API_KEY = os.getenv("NOAA_API_KEY")
headers = {"token": NOAA_API_KEY}
def main():
    db = SessionLocal()
    codes = {row.airport_code for row in db.query(Weather.airport_code).distinct()}
    airports = db.query(Airport).all()
    for row in airports:
        offset = 1
        info = {}
        if row.iata_code not in codes:
            while True:
                data = requests.get(f"https://www.ncei.noaa.gov/cdo-web/api/v2/data?stationid={row.noaa_station_id}&datasetid=GHCND&startdate=2025-01-01&enddate=2026-01-01&datatypeid=PRCP&datatypeid=SNWD&datatypeid=TMAX&datatypeid=TMIN&datatypeid=AWND&offset={offset}&limit=1000", headers=headers)
                print(data.status_code, data.text)
                if not data.text:
                    break
                results_json = data.json()
                if "results" not in results_json:
                    break
                results = results_json["results"]
                for i in results:
                    if i["date"] not in info:
                        info[i["date"]] = {}
                    if i["datatype"] == "PRCP":
                        info[i["date"]]["rain"] = i["value"]
                    elif i["datatype"] == "SNWD":
                        info[i["date"]]["snow_depth"] = i["value"]
                    elif i["datatype"] == "TMAX":  
                        info[i["date"]]["max_temp"] = i["value"]
                    elif i["datatype"] == "TMIN":
                        info[i["date"]]["min_temp"] = i["value"]
                    elif i["datatype"] == "AWND":
                        info[i["date"]]["wind_speed"] = i["value"]
                if len(results) < 1000:
                    break
                if len(results) == 1000:
                    offset += 1000
        for i in info:
            new_weather = Weather(airport_code = row.iata_code, date = i, rain = info[i].get("rain"), snow_depth = info[i].get("snow_depth"), max_temp = info[i].get("max_temp"), min_temp =  info[i].get("min_temp"), wind_speed = info[i].get("wind_speed"))
            db.add(new_weather)
        db.commit()
if __name__ == "__main__":
    main()
