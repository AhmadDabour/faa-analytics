from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from app.models.airport import Airport
from app.database import get_db
router_airport = APIRouter()
@router_airport.get("/airports")
def get_airports(page: int = Query(1, ge=1), limit: int = Query(10, ge=1, le=75), db: Session = Depends(get_db)):
    offset = (page - 1) * limit
    result = db.query(Airport).offset(offset).limit(limit).all()
    if not result:
        raise HTTPException(status_code=404, detail="Item not found")
    return result