from fastapi.testclient import TestClient
from app.main import app
call = TestClient(app)
def test_by_airline():
    response = call.get("analytics/delays/by-airline?limit=10")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert "airline_name" in data[0]
    
def test_by_route():
    response = call.get("analytics/delays/by-route?limit=10")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data,list)
    assert "flight_route" in data[0]

def test_by_month():
    response = call.get("analytics/delays/by-month")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert "month_num" in data[0]
def test_by_weather():
    response = call.get("analytics/by-weather?airport_code=JFK")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert "airline_code" in data[0]

def test_by_best_perform():
    response = call.get("analytics/delays/best-performers?origin=JFK&dest=LAX&limit=10")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert "origin_code" in data[0]

def test_by_cancellations():
    response = call.get("analytics/cancellations/by-airline?airline=AA")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert "airline_name" in data[0]
