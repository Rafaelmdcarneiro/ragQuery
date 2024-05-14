from fastapi import  Response

from starlette.middleware.base import BaseHTTPMiddleware

from corelib.utils.logger_factory import LoggerFactory
from corelib.utils.configuration_builder import Settings
from fastapi.exceptions import RequestValidationError

class AuthenticationMiddleware(BaseHTTPMiddleware):
    '''
    This middleware authenticates requests made to api using the api key
    '''
    
    key = None
    bypass_auth = False
    def __init__(self, app, settings:Settings):
        super().__init__(app)
        if  settings.api_key == None or len(settings.api_key)<1:
            raise ValueError('API key is not configured')
        
        self.key = settings.api_key
        self.bypass_auth = settings.bypass_auth


    async def dispatch(self, request, call_next)->Response:
        
        if (not self.bypass_auth and request.url.path != '/healthcheck' and         
            ('api-key' not in  request.headers or request.headers['api-key'] != self.key )
        ):
            raise RequestValidationError(f"Request can't be authenticated, Host: {request.client.host}")

        response = await call_next(request)
    
        return response