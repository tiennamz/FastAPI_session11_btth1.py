from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base
from database import engine

Base = declarative_base()

class ParkingModel(Base):
    __tablename__ = 'parking_slots'
    id= Column(Integer, primary_key=True, index=True)
    slot_code= Column(String(50), unique=True, nullable=False)
    zone_name= Column(String(255), nullable=False)
    max_weight= Column(Integer, nullable=False)
    is_available= Column(Boolean, default=1)

Base.metadata.create_all(bind=engine)