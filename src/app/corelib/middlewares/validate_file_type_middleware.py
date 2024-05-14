import re

from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from corelib.utils.configuration_builder import Settings



def get_content_type_from_body(body):
    content_type_match = re.search(rb'Content-Type: ([^\r\n]+)', body)

    if content_type_match:
        content_type = content_type_match.group(1).decode("utf-8")
    return content_type

async def set_body(request: Request, body: bytes):
    async def receive():
        return {"type": "http.request", "body": body}
    request._receive = receive


async def get_body(request: Request) -> bytes:
    body = await request.body()
    await set_body(request, body)
    return body


class ValidateContentTypeMiddleware(BaseHTTPMiddleware):
    """
    This middleware intercepts all file uploads and checks if the file type is part of allowed file types or not
    """
    accepted_file_types = []
    def __init__(self, app, settings:Settings):
        super().__init__(app)
        self.accepted_file_types = settings.accepted_file_types

    async def dispatch(self, request: Request, call_next):
        content_type = request.headers.get("Content-Type", "")
        file_content_type = ''

        if content_type.startswith("multipart/form-data"):
            bd = await request.body()
            file_content_type = get_content_type_from_body(bd)

        if file_content_type:
            for route in request.app.routes:

                if hasattr(route,'tags'):
                    if "FileUpload" in route.tags:
                        valid_content_type = file_content_type in self.accepted_file_types
                        if not valid_content_type:
                            raise HTTPException(
                                detail=f'File of type {file_content_type} not supported for upload',
                                status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
                       


        response = await call_next(request)
        return response
