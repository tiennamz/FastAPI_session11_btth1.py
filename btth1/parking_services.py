from sqlalchemy.orm import Session
from models import ParkingModel
from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder


def create_parking_service(db: Session, slot_code: str, zone_name: str, max_weight: int, is_available: bool):
    try:
        new_parking = ParkingModel(
            slot_code=slot_code,
            zone_name=zone_name,
            max_weight=max_weight,
            is_available=is_available
        )
        existed_parking = db.query(ParkingModel).filter(ParkingModel.slot_code == slot_code).first()
        if existed_parking:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Slot code existed'
            )
            
        db.add(new_parking)
        db.commit()
        db.refresh(new_parking)
        return new_parking
    
    except Exception as e: 
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=str(e)
        )


def get_all_parking(db: Session):
    list_parking = db.query(ParkingModel).all()
    list_parking = jsonable_encoder(list_parking)
    return list_parking

def get_parking_by_id_service(db: Session, id: int):
    parking = db.query(ParkingModel).filter(ParkingModel.id == id).first()
    if not parking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='ID not found'
        )
    parking = jsonable_encoder(parking)
    return parking