from sqlalchemy import Column, Integer, String, Float
from  sqlalchemy.orm import declarative_base
from database import engine


Base = declarative_base()

class PlanModel(Base):
    __tablename__ = 'smart_home_plans'
    id = Column(Integer, primary_key=True)
    plan_code = Column(String(50), nullable=False, unique=True)
    plan_name = Column(String(255), nullable=False)
    device_quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    
Base.metadata.create_all(bind=engine)