from pydantic import BaseModel
class AirlineDelayResponse(BaseModel):
    airline_name: str
    total_flights: str
    delay_percentage: float

class RouteDelayResponse(BaseModel):
    flight_route: str
    total_flights: str
    delay_percentage: float

class MonthDelayResponse(BaseModel):
    month_num: int
    total_flights: str
    delay_percentage: float
class WeatherDelayResponse(BaseModel):
    airline_code: str
    rain_total: str
    rain_delay: float
    snow_total: str
    snow_delay: float
    total_delayed_flights: float
class AirlinePerformanceResponse(BaseModel):
    origin_code: str
    destination_code: str
    avg_carrier_delay: float
    avg_weather_delay: float
    airline_name: str
class AirlineFlightCancelResponse(BaseModel):
    airline_name: str
    overall_delay: float
    carrier_delay: float
    weather_delay: float
    security_delay: float
    nas_delay: float
    