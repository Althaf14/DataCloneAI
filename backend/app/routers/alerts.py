from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from .. import crud, schemas, database
from .auth import get_current_user

router = APIRouter(
    prefix="/api/alerts",
    tags=["Alerts"]
)

@router.get("/", response_model=List[schemas.Alert])
def read_alerts(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db), current_user = Depends(get_current_user)):
    alerts = crud.get_alerts(db, skip=skip, limit=limit)
    return alerts
