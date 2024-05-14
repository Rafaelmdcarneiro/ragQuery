from uuid import UUID
import uuid
from sqlalchemy.orm import Session
from datetime import timezone, datetime

from corelib.models import entities
from corelib.models import dtos
from corelib.models.constants import Statuses



def get_document(db: Session, document_id: UUID):
    return db.query(entities.Document).filter(entities.Document.id == document_id).first()


def get_documents(db: Session, skip: int = 0, limit: int = 100):
    return db.query(entities.Document).offset(skip).limit(limit).all()


def create_document(db: Session, document: dtos.DocumentDTO):
   
    db_document = entities.Document()
    db_document.id = uuid.uuid4()
    db_document.file_name = document.file_name
    db_document.file_url = document.file_url
    db_document.file_upload_status = document.file_upload_status
    now = datetime.now(timezone.utc)
    db_document.created = now
    db_document.updated = now

    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    return db_document

def delete_documents(db: Session):
    db.query(entities.Document).delete()
    db.commit()
