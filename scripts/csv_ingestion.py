import csv
import os 
from app.database import SessionLocal
from app.models import Airline
from app.models import Airport
from app.models import Route
from app.models import Flight
import glob
from datetime import datetime
csv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "raw")
file_list = glob.glob(os.path.join(csv_path, "**", "*.csv"), recursive=True)
seen_airlines = set()
seen_airplanes = set()
seen_routes = set()
AIRLINE_NAMES = {
    "AA": "American Airlines",
    "AS": "Alaska Airlines",
    "B6": "JetBlue Airways",
    "DL": "Delta Air Lines",
    "F9": "Frontier Airlines",
    "G4": "Allegiant Air",
    "HA": "Hawaiian Airlines",
    "MQ": "Envoy Air",
    "NK": "Spirit Airlines",
    "OH": "PSA Airlines",
    "OO": "SkyWest Airlines",
    "UA": "United Airlines",
    "WN": "Southwest Airlines",
    "YX": "Republic Airways",
}
def insert_airline(iata_code: str, db):
    if iata_code not in seen_airlines:
        seen_airlines.add(iata_code)
        new_airline = Airline(iata_code = iata_code, name = AIRLINE_NAMES.get(iata_code,"Unkown"))
        db.add(new_airline)
        db.commit()
def insert_airport(iata_code: str, city: str, state: str, db):
    if iata_code not in seen_airplanes:
        seen_airplanes.add(iata_code)
        new_airport = Airport(iata_code = iata_code, city = city, state = state)
        db.add(new_airport)
        db.commit()
def insert_route(origin_code: str, dest_code: str, db):
    if (origin_code, dest_code) not in seen_routes:
        seen_routes.add((origin_code, dest_code))
        new_route = Route(origin_code = origin_code, dest_code = dest_code)
        db.add(new_route)
        db.commit()
def insert_flight(row: dict, db):
        new_date = datetime.strptime(row["FL_DATE"], "%m/%d/%Y %I:%M:%S %p").date()
        new_airline = row["OP_UNIQUE_CARRIER"]
        new_origin_airport = row["ORIGIN"]
        new_dest_airport = row["DEST"]
        new_fl_number = int(float(row["OP_CARRIER_FL_NUM"]))
        if row["CRS_DEP_TIME"] == "":
            new_crs_dep_time = None
        else:
            new_crs_dep_time = int(float(row["CRS_DEP_TIME"]))
        if row["DEP_TIME"] == "":
            new_actual_dep_time = None
        else:
            new_actual_dep_time = int(float(row["DEP_TIME"]))
        if row["DEP_DELAY"] == "":
            new_dep_delay = None
        else:
            new_dep_delay = float(row["DEP_DELAY"])
        if row["DEP_DEL15"] == "0.00":
            new_dep_del = False
        elif row["DEP_DEL15"] == "1.00":
            new_dep_del = True
        else:
            new_dep_del = None
        if row["ARR_TIME"] == "":
            new_actual_arr_time = None
        else:
            new_actual_arr_time = int(float(row["ARR_TIME"]))
        if row["CRS_ARR_TIME"] == "":
            new_crs_arr_time = None
        else:
            new_crs_arr_time = int(float(row["CRS_ARR_TIME"]))
        if row["ARR_DELAY"] == "":
            new_arr_delay = None
        else:
            new_arr_delay = float(row["ARR_DELAY"])
        if row["ARR_DEL15"] == "0.00":
            new_arr_del = False
        elif row["ARR_DEL15"] == "1.00":
            new_arr_del = True
        else:
            new_arr_del = None
        if row["CANCELLED"] == "0.00":
            new_cancelled = False
        elif row["CANCELLED"] == "1.00":
            new_cancelled = True
        else:
            new_cancelled = None
        new_cancel_code = row["CANCELLATION_CODE"]
        if row["DIVERTED"] == "0.00":
            new_diverted = False
        elif row["DIVERTED"] == "1.00":
            new_diverted = True
        else:
            new_diverted = None
        if row["CRS_ELAPSED_TIME"] == "":
            new_crs_elap_time = None
        else:
            new_crs_elap_time = int(float(row["CRS_ELAPSED_TIME"]))
        if row["ACTUAL_ELAPSED_TIME"] == "":
            new_actual_elap_time = None
        else:
            new_actual_elap_time = int(float(row["ACTUAL_ELAPSED_TIME"]))
        if row["AIR_TIME"] == "":
            new_air_time = None
        else:
            new_air_time = float(row["AIR_TIME"])
        new_distance = float(row["DISTANCE"])
        if row["CARRIER_DELAY"] == "":
            new_carrier_delay = None
        else:
            new_carrier_delay = float(row["CARRIER_DELAY"])
        if row["WEATHER_DELAY"] == "":
            new_weather_delay = None
        else:
            new_weather_delay = float(row["WEATHER_DELAY"])
        if row["NAS_DELAY"] == "":
            new_nas_delay = None
        else:
            new_nas_delay = float(row["NAS_DELAY"])
        if row["SECURITY_DELAY"] == "":
            new_security_delay = None
        else:
            new_security_delay = float(row["SECURITY_DELAY"])
        if row["LATE_AIRCRAFT_DELAY"] == "":
            new_aircraft_delay = None
        else:
            new_aircraft_delay = float(row["LATE_AIRCRAFT_DELAY"])
        new_flight = Flight(date = new_date,airline_code = new_airline, origin_airport = new_origin_airport, dest_airport =  new_dest_airport, flight_number = new_fl_number, scheduled_dep_time = new_crs_dep_time, actual_dep_time = new_actual_dep_time, dep_delay = new_dep_delay, dep_delay_15 = new_dep_del, arr_time = new_actual_arr_time, scheduled_arr_time = new_crs_arr_time, arr_delay = new_arr_delay, arr_delay_15 = new_arr_del, cancelled = new_cancelled, cancellation_code = new_cancel_code, diverted = new_diverted, scheduled_elapsed_time = new_crs_elap_time, actual_elapsed_time = new_actual_elap_time, air_time = new_air_time, distance = new_distance, carrier_delay = new_carrier_delay, weather_delay = new_weather_delay, nas_delay =  new_nas_delay, security_delay = new_security_delay, late_aircraft_delay = new_aircraft_delay)
        db.add(new_flight)
db = SessionLocal()
counter = 0
for i in file_list:
    with open(i, 'r', encoding="utf8") as f:
        reader = csv.DictReader(f)
        for row in reader: 
            try:
                insert_airline(row["OP_UNIQUE_CARRIER"], db)
                insert_airport(row["ORIGIN"], row["ORIGIN_CITY_NAME"], row["ORIGIN_STATE_ABR"], db)
                insert_airport(row["DEST"], row["DEST_CITY_NAME"], row["DEST_STATE_ABR"], db)
                insert_route(row["ORIGIN"], row["DEST"], db)
                insert_flight(row, db)
                counter += 1
                if counter >= 1000:
                    db.commit()
                    counter = 0
            except Exception as e:
                print(f"Erorr: {e}")
                break
db.commit()