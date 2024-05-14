from typing import Union
from typing_extensions import Annotated
from uuid import UUID

from pydantic import BaseModel

from corelib.models.constants import Statuses


class DocumentDTO(BaseModel):
    id : Union[UUID, None] = None
    file_name : str 
    file_url : str
    file_upload_status : Union[Statuses,None] = None
    file_type :str
    file_size : str
    ocr_status : Union[Statuses,None] = None
    ocr_file_url : Union[str,None] = None
    embedding_status : Union[Statuses,None] = None

    class Config:
        orm_mode = True
