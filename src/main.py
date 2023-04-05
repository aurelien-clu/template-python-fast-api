import time

from fastapi import Request
from fastapi.responses import JSONResponse

from src import logger
from src.app import create_app
from src.errors import SomethingIsNotRight

app = create_app()


@app.exception_handler(SomethingIsNotRight)
async def too_few_documents_exception_handler(request: Request, exc: SomethingIsNotRight):
    msg = "Something was not right, our deepest apology"
    return JSONResponse(status_code=599, content={"message": msg})


@app.exception_handler(Exception)
async def exception_handler(request: Request, exc: Exception):
    msg = "Internal server error"
    return JSONResponse(status_code=500, content={"message": msg})


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time  # in seconds
    response.headers["X-Process-Time"] = str(process_time)
    logger.debug(f"response took {process_time} seconds")
    return response
