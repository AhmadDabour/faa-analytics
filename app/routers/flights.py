from fastapi import APIRouter, Depends, Query, HTTPException
from app.database import get_db
from sqlalchemy.orm import Session
from app.models.flight import Flight
router_flight = APIRouter()
@router_flight.get("/flights")
def get_flights(page: int = Query(1, ge=1), limit: int = Query(10, ge=1, le=75), db: Session = Depends(get_db)):
    offset = (page - 1) * limit
    result = db.query(Flight).offset(offset).limit(limit).all()
    if not result:
        raise HTTPException(status_code=404, detail= "Item not found")
    return result
