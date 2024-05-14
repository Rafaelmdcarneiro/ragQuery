from fastapi import Response

from starlette.middleware.base import BaseHTTPMiddleware

from corelib.utils.logger_factory import LoggerFactory
from corelib.utils.configuration_builder import Settings

class BaseRequestLoggingMiddleware(BaseHTTPMiddleware):
    '''
    This middleware logs all the requests that are being made to the API
    '''
    
    logger = None
    def __init__(self, app, settings:Settings):
        super().__init__(app)
        self.logger = LoggerFactory().get_logger(settings=settings)


    async def dispatch(self, request, call_next)->Response:
          
        response = await call_next(request)
        self.logger.info(f"A new request pipeline initiated by {request.client.host}")

        return response