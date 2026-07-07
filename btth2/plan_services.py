from sqlalchemy.orm import Session
from models import PlanModel
from fastapi.encoders import jsonable_encoder


def create_plan_services(db: Session, plan_code: str, plan_name: str, device_quantity: int, price: float):

    new_plan = PlanModel(
        plan_code=plan_code, 
        plan_name=plan_name, 
        device_quantity= device_quantity,
        price=price
    )
    existed_code = db.query(PlanModel).filter(PlanModel.plan_code == plan_code).first()
    
    if existed_code:
        return None
    
    db.add(new_plan)
    db.commit()
    db.refresh(new_plan)
    return new_plan

def get_all_plans_services(db: Session):
    plans = db.query(PlanModel).all()
    plans = jsonable_encoder(plans)
    return plans

def get_plan_by_id_services(db: Session, id: int):
    plan = db.query(PlanModel).filter(PlanModel.id == id).first()
    if not plan:
        return None
    plan = jsonable_encoder(plan)
    return plan