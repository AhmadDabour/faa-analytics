from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, case, or_, extract, and_, desc
from app.database import get_db
from app.models.flight import Flight
from app.models.airline import Airline
from app.models.weather import Weather
from typing import List
from app.schemas import AirlineDelayResponse, RouteDelayResponse, MonthDelayResponse, WeatherDelayResponse, AirlinePerformanceResponse, AirlineFlightCancelResponse
from app.redis_client import r
import json
router_analytics = APIRouter()
@router_analytics.get("/analytics/delays/by-airline", response_model=List[AirlineDelayResponse])
def get_analytics_by_airline(limit: int, db: Session = Depends(get_db)):
    cache_key = f"analytics:by_airline:{limit}"
    try:
        res = r.get(cache_key)
    except Exception as e:
        print(f"Redis error: {e}")
        res = None
    if res is None:
        delayed_flights = (
        db.query(
            Flight.airline_code,
            Airline.name,
            func.count(
                case(
                    (or_(Flight.dep_delay_15 == True, Flight.arr_delay_15 == True), 1),
                    else_=None
                ) 
            ), func.count(),
        ).join(Airline, Flight.airline_code == Airline.iata_code)
            .group_by(Flight.airline_code, Airline.name).limit(limit).all()
        )

        airlines = []
        for row in delayed_flights:
            delay_percentage = (row[2] / row[3]) * 100
            airlines.append({ "airline_name": row[1], "total_flights": f"{row[2]}/{row[3]}", "delay_percentage": round(delay_percentage, 2)})
        data = json.dumps(airlines)
        try:
             r.set(cache_key, data, ex=3600)
        except Exception:
             pass
    else:
        airlines = json.loads(res)
    if not airlines:
        raise HTTPException(status_code=404, detail="Item not found")
    return airlines
        
            
@router_analytics.get("/analytics/delays/by-route", response_model= List[RouteDelayResponse])
def get_analytics_by_route(limit: int, db: Session = Depends(get_db)):
    cache_key = f"analytics:by_route:{limit}"
    try:
        res = r.get(cache_key)
    except Exception as e:
        print(f"Redis error: {e}")
        res = None
    if res is None:
        delayed_routes = (
            db.query(Flight.origin_airport, Flight.dest_airport,
                    func.count( 
                        case ( 
                            (or_(Flight.dep_delay_15 == True, Flight.arr_delay_15 == True), 1),
                            else_= None
                    )
                    ), func.count()
            )
            .group_by(Flight.origin_airport, Flight.dest_airport).limit(limit).all()
        )
        routes = []
        for row in delayed_routes:
            delay_percentage = (row[2] / row[3]) * 100
            routes.append({"flight_route": f"{row[0]} --> {row[1]}", "total_flights": f"{row[2]}/{row[3]}", "delay_percentage": round(delay_percentage, 2)})
        data = json.dumps(routes)
        try:
             r.set(cache_key, data, ex=3600)
        except Exception:
             pass
    else:
        routes = json.loads(res)
    if not routes:
        raise HTTPException(status_code=404, detail="Item not found")
    return routes

@router_analytics.get("/analytics/delays/by-month", response_model=List[MonthDelayResponse])
def get_analytics_by_month(db: Session = Depends(get_db)):
    cache_key = "analytics:by_month"
    try:
        res = r.get(cache_key)
    except Exception as e:
        print(f"Redis error: {e}")
        res = None
    if res is None:
        delayed_months = db.query(extract("month", Flight.date),
                    func.count(
                    case(
                        (or_(Flight.dep_delay_15 == True, Flight.arr_delay_15 == True), 1),
                        else_= None
                    )
                ), func.count()
                ).group_by(extract("month", Flight.date)).all()
        months = []
        for row in delayed_months:
            delay_percentage = (row[1] / row[2]) * 100
            months.append({"month_num": int(row[0]), "total_flights": f"{row[1]}/{row[2]}", "delay_percentage": round(delay_percentage, 2)})
        data = json.dumps(months)
        try:
             r.set(cache_key, data, ex=3600)
        except Exception:
             pass    
    else:
        months = json.loads(res)
    if not months:
        raise HTTPException(status_code=404, detail="Item not found")
    return months

@router_analytics.get("/analytics/by-weather", response_model=List[WeatherDelayResponse]) 
def get_analytics_by_weather(airport_code: str, db: Session = Depends(get_db)):
    cache_key = f"analytics:by_weather:{airport_code}"
    try:
        res = r.get(cache_key)
    except Exception as e:
        print(f"Redis error: {e}")
        res = None
    if res is None:
         delayed_weather = db.query(Flight.origin_airport,
                    func.count(
                        case(
                             (Weather.rain > 0,1),
                        else_=None
                        )
                        )
                        ,
                        func.count(
                             case(
                                (and_(Weather.rain > 0, or_(Flight.arr_delay_15 == True, Flight.dep_delay_15 == True)), 1),
                                else_=None
                            )
                            ),
                        func.count(
                            case(
                                (Weather.snow_depth > 0, 1),
                                else_=None
                                )
                        ), func.count(
                             case(
                                (and_(Weather.snow_depth > 0, or_(Flight.arr_delay_15 == True, Flight.dep_delay_15 == True)), 1),
                                else_=None
                            )
                            ),
                            func.count(
                                case(
                                    (or_(Flight.dep_delay_15 == True, Flight.arr_delay_15 == True), 1),
                                    else_=None
                                    )
                            ),
                            func.count()
                            ).join(Weather, and_(Weather.airport_code == Flight.origin_airport, Weather.date == Flight.date)).filter(Flight.origin_airport == airport_code).group_by(Flight.origin_airport).all()
         weather_data = []
         for row in delayed_weather:
             rain_delay = (row[2] / row[1]) * 100 if row[1] != 0 else 0.00
             snow_delay = (row[4] / row[3]) * 100 if row[3] != 0 else 0.00
             total_flights = (row[5] / row[6]) * 100 if row[6] != 0 else 0.00
             weather_data.append({"airline_code": row[0], "rain_delay": round(rain_delay, 2), "rain_total": f"{row[2]}/{row[1]}", "snow_delay": round(snow_delay, 2),"snow_total": f"{row[4]}/{row[3]}", "total_delayed_flights": round(total_flights, 2)})
         data = json.dumps(weather_data)
         try:
             r.set(cache_key, data, ex=3600)
         except Exception:
             pass
    else:
        weather_data = json.loads(res)
    if not weather_data:
        raise HTTPException(status_code=404, detail="Item not found")
    return weather_data

@router_analytics.get("/analytics/delays/best-performers", response_model=list[AirlinePerformanceResponse])
def get_best_performers(origin: str, dest: str, limit: int = 10, db: Session = Depends(get_db)):
    cache_key = f"analytics:best_performers:{origin}:{dest}"
    try:
        res = r.get(cache_key)
    except Exception as e:
        print(f"Redis error: {e}")
        res = None
    if res is None:
        route_delay = db.query(Flight.origin_airport, Flight.dest_airport, func.avg(Flight.carrier_delay), func.avg(Flight.weather_delay), Flight.airline_code, Airline.name
                               
                               ).join(Airline, Flight.airline_code == Airline.iata_code).filter(and_(Flight.origin_airport == origin, Flight.dest_airport == dest)
                                        ).group_by(Flight.origin_airport, Flight.dest_airport, Flight.airline_code, Airline.name
                                                   ).having(func.count(Flight.origin_airport) >= 5
                                                            ).order_by(func.avg(Flight.carrier_delay).asc()).limit(limit).all()
        route_data = []
        for row in route_delay:
            route_data.append({"origin_code": row[0], "destination_code": row[1], "avg_carrier_delay": round(row[2], 2) if row[2] is not None else 0.00, "avg_weather_delay": round(row[3], 2) if row[3] is not None else 0.00, "airline_name": row[5]})
        data = json.dumps(route_data)
        try:
             r.set(cache_key, data, ex=3600)
        except Exception:
             pass
    else:
        route_data = json.loads(res)
    if not route_data:
        raise HTTPException(status_code=404, detail="Item not found")
    return route_data

@router_analytics.get("/analytics/cancellations/by-airline", response_model= list[AirlineFlightCancelResponse])
def get_cancellations_by_airline(airline: str = None, db: Session = Depends(get_db)):
    cache_key = f"analytics:cancellations:by_airline:{airline}"
    try:
        res = r.get(cache_key)
    except Exception as e:
        print(f"Redis error: {e}")
        res = None
    if res is None:
        query = db.query(Airline.name,
                 func.count( 
                     case( 
                         (Flight.cancellation_code == "A", 1),
                         else_=None
                     )
                 ),
                 func.count(
                     case(
                         (Flight.cancellation_code == "B", 1),
                         else_=None
                     )
                 ),
                 func.count(
                     case( 
                         (Flight.cancellation_code == "C", 1),
                         else_=None
                     )
                 ),
                 func.count(
                     case(
                         (Flight.cancellation_code == "D", 1),
                         else_=None
                     )
                 ),
                 func.count(
                     case(
                         (Flight.cancelled == True, 1),
                         else_=None
                     )
                 ),
                 func.count()
                 
                 ).join(Airline, Flight.airline_code == Airline.iata_code
                 ).group_by(Airline.name).order_by(desc((func.count(case((Flight.cancelled == True, 1), else_=None)) / func.count()) * 100))
        if airline is not None:
            query = query.filter(Flight.airline_code == airline)
        cancelled_data = query.all()
        cancellations = []
        for row in cancelled_data:
            carrier_delay = (row[1] / row[5]) * 100 if row[5] != 0 else 0.00
            weather_delay = (row[2] / row[5]) * 100 if row[5] != 0 else 0.00
            nas_delay = (row[3] / row[5]) * 100 if row[5] != 0 else 0.00
            security_delay = (row[4] / row[5] ) * 100 if row[5] != 0 else 0.00
            overall_delay = (row[5] / row[6]) * 100
            cancellations.append({"airline_name": row[0], "overall_delay": round(overall_delay, 2), "carrier_delay": round(carrier_delay, 2) , "weather_delay":round(weather_delay, 2), "security_delay": round(security_delay, 2), "nas_delay": round(nas_delay, 2)})
        data = json.dumps(cancellations)
        try:
             r.set(cache_key, data, ex=3600)
        except Exception:
             pass
    else:
        cancellations = json.loads(res)
    if not cancellations:
        raise HTTPException(status_code=404, detail="Item not found")
    return cancellations

