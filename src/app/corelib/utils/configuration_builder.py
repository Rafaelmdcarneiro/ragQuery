from pydantic_settings import BaseSettings, SettingsConfigDict 
import os
from pathlib import Path
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv(".env"))

class Settings(BaseSettings):
    """
    This class instantiates settings for the entire application
    """

    app_name:str = "default"
    api_version:str = "0.1"
    api_key: str = 'DUMMYKEY'

    log_file:str = 'api.log'
    log_level: str = 'INFO'
    logger_type:str = 'FILE'

    sqllite_db_url:str = "sqlite:///./sql_app.db"

    bypass_auth:bool = False

    minio_url:str = "127.0.0.1:9001"
    minio_access_key:str = "minioadmin"
    minio_secret_key:str = "minioadmin"

    file_upload_bucket:str = "UploadData"
    file_ocr_bucket:str = "OCRData"
    accepted_file_types:list[str] = ["application/pdf","image/jpeg","image/png","image/tiff"]

    class Config:
        env_file = find_dotenv(".env")
    #model_config = SettingsConfigDict(env_file=load_dotenv(find_dotenv(".env")))

    
class TestSettings(BaseSettings):
    """
    This class instantiates settings for running tests
    """

    app_name:str = "default"
    api_version:str = "0.1"
    api_key: str = 'DUMMYKEY'

    log_file:str = 'api.log'
    log_level: str = 'INFO'
    logger_type:str = 'FILE'

    sqllite_db_url:str = "sqlite:///./sql_app.db"

    bypass_auth:bool = False

    minio_url:str = "127.0.0.1:9001"
    minio_access_key:str = "minioadmin"
    minio_secret_key:str = "minioadmin"

    
    file_upload_bucket:str = "UploadData"
    file_ocr_bucket:str = "OCRData"
    accepted_file_types:list

    

    model_config = SettingsConfigDict(env_file=load_dotenv(find_dotenv(".env.test")))
    
        


   




