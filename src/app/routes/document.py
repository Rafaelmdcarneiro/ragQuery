from fastapi import APIRouter, Depends,Request, UploadFile,status
from corelib.models.dtos import DocumentDTO
from corelib.models.constants import Statuses
from sqlalchemy.orm import Session
from corelib.utils.dependencies import create_logger, get_settings, get_sqllite_db
from corelib.middlewares.base_request_logging_middleware import BaseRequestLoggingMiddleware
from corelib.utils.configuration_builder import Settings
from corelib.utils.logger_factory import LoggerFactory
from corelib.repositories import document_repo as dr_repo

from typing_extensions import Annotated
from uuid import UUID
import logging


router = APIRouter(
prefix="/document",
tags=["document"],
responses={404: {"description": "Not found"},
           500:{"description":"Something went wrong"}}
)


@router.get("/", response_model=list[DocumentDTO])
async def test(db:Session = Depends(get_sqllite_db)):

    doc = DocumentDTO( file_name='test2', file_url='abc.net')
    doc.file_upload_status = Statuses.Success.value

    dr_repo.create_document(db,doc)

    return dr_repo.get_documents(db)



@router.post("/upload/", tags=['FileUpload'])
async def upload_file(file: UploadFile, settings:Settings=Depends(get_settings))->str:
    """
    This endpoint is used for uploading files to blob storage
    """

    file_type = file.content_type

    return "ghghg"


@router.get("/info/")
async def read_file_info():
    return "fileinfo"


@router.post("/ocr/{id}")
async def run_ocr(id:UUID):
    return "ocr completed"


@router.post("/extract/")
async def extract_attribute(id:UUID):
    return "ocr completed"


