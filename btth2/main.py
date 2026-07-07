from fastapi import FastAPI, Request, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import get_db
from plan_services import create_plan_services, get_all_plans_services, get_plan_by_id_services
from response import create_response
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

app = FastAPI()

@app.exception_handler(HTTPException)
def http_exception_handler(
    request: Request,
    exc: HTTPException
):
    response = create_response(request, exc.status_code, 'Failed', error=exc.detail)
    return JSONResponse(
        status_code=exc.status_code,
        content=response.model_dump()
    )

@app.exception_handler(Exception)
def global_exception_handler(
    request: Request,
    exc: Exception
):
    response = create_response(request, status.HTTP_500_INTERNAL_SERVER_ERROR, 'Failed', error=str(exc))
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=response.model_dump()
    )
    

    
@app.exception_handler(RequestValidationError)
def http_exception_handler(
    request: Request,
    exc: RequestValidationError
):
    response = create_response(request, status.HTTP_422_UNPROCESSABLE_CONTENT, 'Failed', error=exc.errors())
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        content=response.model_dump()
    )
    

class CreatePlans(BaseModel):
    plan_code: str
    plan_name: str
    device_quantity: int
    price: float

@app.post('/smart-home-plans')
def create_plan(request: Request, new_plan: CreatePlans, db: Session = Depends(get_db)):
    plan = create_plan_services(db, new_plan.plan_code, new_plan.plan_name, new_plan.device_quantity, new_plan.price)
        
    if not plan:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='ID existed'
        )
        
    return create_response(request, status.HTTP_201_CREATED, 'Success', plan)

@app.get('/smart-home-plans')
def get_plans(request: Request, db: Session = Depends(get_db)):
    return create_response(request, status.HTTP_200_OK, 'Success', get_all_plans_services(db))

@app.get('/smart-home-plans/{plan_id}')
def get_plan_by_id(plan_id: int, request: Request, db: Session = Depends(get_db)):
    plan = get_plan_by_id_services(db, plan_id)
    if not plan:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail='ID not found'
        )
    return create_response(request, status.HTTP_200_OK, 'Success', plan)
