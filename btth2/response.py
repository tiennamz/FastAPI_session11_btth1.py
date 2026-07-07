from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import Optional, Any
from datetime import datetime



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
    


