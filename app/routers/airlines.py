from fastapi import Depends, APIRouter, Query, HTTPException
from app.database import get_db
from sqlalchemy.orm import Session
from app.models.airline import Airline
router_airline = APIRouter()
@router_airline.get("/airlines")
def get_airlines(page: int = Query(1, ge=1), limit: int = Query(10, ge=1, le=75), db: Session = Depends(get_db)):
    offset = (page - 1) * limit
    result = db.query(Airline).offset(offset).limit(limit).all()
    if not result:
        raise HTTPException(status_code=404, detail="Item not found")
    return result