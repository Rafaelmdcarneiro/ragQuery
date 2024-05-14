
from sqlalchemy import Boolean, Column, Integer, String, UUID, DateTime
from corelib.models.constants import Statuses
from corelib.db.sqllitebase  import SQLLiteBase
from corelib.utils.dependencies import get_settings

sqllite_base = SQLLiteBase(get_settings()) 
Base = sqllite_base.Base

class Document(Base):
    __tablename__ = "documents"

    id = Column(UUID, primary_key=True)
    file_name = Column(String,index=True,nullable=False)
    file_url = Column(String,index=True,nullable=False)
    file_upload_status = Column(Integer,nullable=False)
    file_type = Column(String,nullable=False)
    file_size = Column(Integer,nullable=False)
    ocr_status = Column(Integer,nullable=True)
    ocr_file_url = Column(String,index=True,nullable=True)
    embedding_status = Column(Integer,nullable=True)
    created = Column(DateTime,nullable=False)
    updated = Column(DateTime,nullable=False)




