from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import OperationalError, ProgrammingError

app = FastAPI()

@app.exception_handler(OperationalError)
async def operational_error_handler(request: Request, exc: OperationalError):
    
    return JSONResponse(
        status_code=503,
        content={"detail": "Проблема с базой данных. Попробуйте позже."},
    )

@app.exception_handler(ProgrammingError)
async def programming_error_handler(request: Request, exc: ProgrammingError):
    return JSONResponse(
        status_code=500,
        content={"detail": "Внутренняя ошибка сервера"},
    )

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": "Внутренняя ошибка сервера"},
    )