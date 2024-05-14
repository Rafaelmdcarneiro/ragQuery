from dotenv import load_dotenv
from fastapi.responses import PlainTextResponse
import uvicorn
from fastapi import FastAPI, Depends,Request,status
from corelib.middlewares.validate_file_type_middleware import ValidateContentTypeMiddleware
from corelib.db.sqllitebase import SQLLiteBase
from corelib.middlewares.exception_handler_middleware import ExceptionHandlerMiddleware
from corelib.middlewares.authentication_middleware import AuthenticationMiddleware
from corelib.utils.dependencies import create_logger, get_settings
from corelib.middlewares.base_request_logging_middleware import BaseRequestLoggingMiddleware
from corelib.utils.configuration_builder import Settings
from typing_extensions import Annotated
from corelib.models import entities
import logging

from routes import document

#load_dotenv()

sqllite_base = SQLLiteBase(get_settings())
entities.Base.metadata.create_all(bind=sqllite_base.engine)

app = FastAPI()

# Include app routes BEGIN
app.include_router(document.router)
# Include app routes END


# MIDDLEWARES BEGIN

app.add_middleware(ValidateContentTypeMiddleware,settings=get_settings())
app.add_middleware(AuthenticationMiddleware,settings=get_settings())
app.add_middleware(BaseRequestLoggingMiddleware,settings=get_settings())
# Top most layer exception handler 
app.add_middleware(ExceptionHandlerMiddleware,settings=get_settings())

# MIDDLEWARES END


@app.get("/healthcheck", 
         status_code=status.HTTP_200_OK, 
         summary="Perform health check for the API",
         description="This endpoint is an open end point for checking if the api is running, configurations are getting loaded and logger is working")
async def healthcheck(settings: Annotated[Settings, Depends(get_settings)], log:Annotated[logging.Logger,Depends(create_logger)])->str:
    log.info("Health Check API Called")
    return PlainTextResponse(f"{settings.app_name} working!") 


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)