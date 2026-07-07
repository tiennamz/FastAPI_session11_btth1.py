from fastapi import HTTPException, status, Request, FastAPI
from pydantic import BaseModel
from typing import Optional, Any
from datetime import datetime
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

app = FastAPI()

class BaseResponse(BaseModel):
    status_code: int
    message: str
    data: Optional[Any]
    error: Optional[Any]
    timestamp: str
    path: str
    
    
def create_response(request: Request, status_code: str, message: str, data = None, error = None):
    return BaseResponse(
        status_code=status_code,
        message=message,
        data=data,
        error=error,
        timestamp=datetime.now().isoformat(),
        path=request.url.path
    )
    

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
def validate_error_handler(
    request: Request,
    exc: RequestValidationError
):
    response = create_response(request, status.HTTP_422_UNPROCESSABLE_CONTENT, 'Failed', error=exc.errors())
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        content=response.model_dump()
    )
    
    
    