from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from app.models.route import Route
from app.database import get_db
router_routes = APIRouter()
@router_routes.get("/routes")
def get_routes(page: int = Query(1, ge=1), limit: int = Query(10, ge=1, le=75), db: Session = Depends(get_db)):
    offset = (page - 1) * limit
    result = db.query(Route).offset(offset).limit(limit).all()
    if not result:
        raise HTTPException(status_code=404, detail="Item not found")
    return result