from fastapi import HTTPException, Response

from fastapi.exceptions import RequestValidationError
from starlette.middleware.base import BaseHTTPMiddleware

from corelib.utils.logger_factory import LoggerFactory
from corelib.utils.configuration_builder import Settings

class ExceptionHandlerMiddleware(BaseHTTPMiddleware):
    '''
    This is a global exception handler for the API
    '''
    
    logger = None
    def __init__(self, app, settings:Settings):
        super().__init__(app)
        self.logger = LoggerFactory().get_logger(settings=settings)


    async def dispatch(self, request, call_next)->Response:
        status_code = 200
        try:
            return await call_next(request)
        except RequestValidationError as rve:
            status_code = 401
            # Writing error to logs
            self.logger.error(f"Exception: [Authentication Failed] {rve}")
            return Response("Request can't  be authenticated", status_code=status_code)
        
        except HTTPException as httpExc:
            return Response(httpExc.detail,status_code=httpExc.status_code)
        
        except Exception as e:
            status_code = 500
            # Writing error to logs
            self.logger.error(f"Exception: {e}")
            return Response("Internal server error 2", status_code=status_code)