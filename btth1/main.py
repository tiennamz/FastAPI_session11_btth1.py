from fastapi import FastAPI, Depends, status, Request
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from database import get_db
from response import create_response
from parking_services import create_parking_service, get_all_parking, get_parking_by_id_service


app = FastAPI()

class CreateParkings(BaseModel):
    slot_code: str
    zone_name: str = Field(min_length=3)
    max_weight: int = Field(gt=0)
    is_available: bool = Field(default=1)
    
@app.post('/parking-slots')
def create_parking(request: Request,new_parking: CreateParkings, db: Session = Depends(get_db)):
    created_parking = create_parking_service(db, new_parking.slot_code, new_parking.zone_name, new_parking.max_weight, new_parking.is_available)
    return create_response(request, status.HTTP_201_CREATED, 'Success', created_parking)

@app.get('/parking-slots')
def get_parking(request: Request, db: Session = Depends(get_db)):
    return create_response(request, status.HTTP_200_OK, 'Success', get_all_parking(db))

@app.get('/parking-slots/{slot_id}')
def get_parking_by_id(slot_id: int, request: Request, db: Session = Depends(get_db)):
    return create_response(request, status.HTTP_200_OK, 'Success', get_parking_by_id_service(db, slot_id))
    